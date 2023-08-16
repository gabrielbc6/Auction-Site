from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class Lote(models.Model):
    vendedor = models.CharField(max_length=200)
    nome = models.CharField(max_length=200, unique=True)
    descricao = models.CharField(max_length=200)
    estado = models.CharField(max_length=100)
    valorMinimo = models.FloatField(null=True)
    valorReserva = models.FloatField()
    valorMinimoLance = models.FloatField(null=True)
    inicioLeilao = models.DateField(null=True)
    finalLeilao = models.DateField(null=True)
    tipoInicial = models.IntegerField(null=True)
    tipoFinal = models.IntegerField(null=True)
    confirmado = models.BooleanField(default=False)
    pendente = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome

    def defineTipoInicial(self):
        if (self.valorMinimo <= 1000):
            self.tipoInicial = 1
        elif (self.valorMinimo > 1000 and self.valorMinimo <= 10000):
            self.tipoInicial = 2
        elif (self.valorMinimo > 10000 and self.valorMinimo <= 50000):
            self.tipoInicial = 3
        elif (self.valorMinimo > 50000 and self.valorMinimo <= 100000):
            self.tipoInicial = 4

    def defineTipoFinal(self, valorLance):
        if (valorLance <= 1000):
            self.tipoFinal = 1
        elif (valorLance > 1000 and valorLance <= 10000):
            self.tipoFinal = 2
        elif (valorLance > 10000 and valorLance <= 50000):
            self.tipoFinal = 3
        elif (valorLance > 50000 and valorLance <= 100000):
            self.tipoFinal = 4
    
    def confirmar(self):
        self.confirmado = True
        self.save()
    
    def get_absolute_url(self):
        return reverse('lote:lote_edit', kwargs={'pk': self.pk})

class Leilao(models.Model):
    inicioLeilao = models.DateField()
    finalLeilao = models.DateField()
    maiorLance = models.FloatField(null=True)
    loteLeilao = models.CharField(max_length=200)
    vencedor = models.CharField(max_length=200,default="None")
    pagamentoLeilao = models.CharField(max_length=200)
    liberado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)
    confirmaPagamento = models.BooleanField(default=False)
    cancelar = models.BooleanField(default=False)

    def __str__(self):
        return self.loteLeilao

    def defineMaiorLance(self, novoLance):
        if(self.maiorLance):
            if (self.maiorLance < novoLance):
                self.maiorLance = novoLance
                self.save()
        else:
            self.maiorLance = novoLance
            self.save()
    
    def liberar(self):
        hoje = date.today()
        lote = get_object_or_404(Lote, nome=self.loteLeilao)
        if (lote.confirmado and hoje >= self.inicioLeilao and hoje <= self.finalLeilao):
            self.liberado = True
            self.save()
    
    def finalizar(self, manual):
        hoje = date.today()
        if (manual or (hoje > self.finalLeilao and self.finalizado==False)):
            lote = get_object_or_404(Lote, nome=self.loteLeilao)
            if (self.maiorLance > lote.valorReserva):
                lance = get_object_or_404(Lance, valor=self.maiorLance, leilao=self.id)
                lote.defineTipoFinal(lance.valor)
                lote.save()
                pagamento = Pagamento.objects.create(valor=lance.valor, efetuador=lance.comprador, leilao=self.id)
                pagamento.defineTaxaFinal()
                self.finalizado = True
                self.vencedor = lance.comprador
                self.save()
            else:
                lote.pendente = True
                lote.valorMinimoLance = None
                lote.save()
                lances = Lance.objects.filter(leilao=self.id)
                for lance in lances:
                    lance.delete()
                self.delete()
            
    def rejeitar(self):
        self.cancelar = False
        self.save()
    
    def solicitarCancelamento(self):
        lote = get_object_or_404(Lote, nome=self.loteLeilao)
        if (lote.confirmado and not self.finalizado and not self.liberado):
            self.cancelar = True
            self.save()
        elif (not lote.confirmado):
            self.delete()

    def get_absolute_url(self):
        return reverse('lote:lote_edit', kwargs={'pk': self.pk})

class Lance(models.Model):
    valor = models.FloatField()
    comprador = models.CharField(max_length=200)
    leilao =  models.IntegerField()

    def __str__(self):
        return self.comprador

class Pagamento(models.Model):
    valor = models.FloatField()
    dataDeConfirmacao = models.DateField(null=True)
    efetuador = models.CharField(max_length=200)
    lote = models.IntegerField(null=True, default=None)
    leilao = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.efetuador

    def defineTaxaInicial(self):
        if(self.valor <= 1000):
            taxa = 0.01
        if(self.valor > 1000 and self.valor <= 10000):
            taxa = 0.02
        if(self.valor > 10000 and self.valor <= 50000):
            taxa = 0.03
        if(self.valor > 50000 and self.valor <= 100000):
            taxa = 0.04
        self.valor = self.valor*taxa
        self.save()

    def defineTaxaFinal(self):
        if(self.valor <= 1000):
            taxa = 0.03
        if(self.valor > 1000 and self.valor <= 10000):
            taxa = 0.04
        if(self.valor > 10000 and self.valor <= 50000):
            taxa = 0.05
        if(self.valor > 50000 and self.valor <= 100000):
            taxa = 0.06
        self.valor += self.valor*taxa
        self.save()
