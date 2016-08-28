# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import os
from .comunicacao import executar_consulta
from .assinatura import Assinatura
from pytrustnfe.xml import render_xml
from pytrustnfe.utils import CabecalhoSoap
from pytrustnfe.utils import gerar_chave, ChaveNFe
from pytrustnfe.Servidores import localizar_url


def _build_header(**kwargs):
    vals = {'estado': kwargs['estado'], 'soap_action': ''}
    return CabecalhoSoap(**vals)

def _generate_nfe_id(**kwargs):
    for item in kwargs['NFes']:
        vals = {
            'cnpj': item['infNFe']['emit']['cnpj_cpf'],
            'estado': item['infNFe']['ide']['cUF'],
            'emissao': '%s%s' % (item['infNFe']['ide']['dhEmi'][2:4],
                                 item['infNFe']['ide']['dhEmi'][5:7]),
            'modelo': item['infNFe']['ide']['mod'],
            'serie': item['infNFe']['ide']['serie'],
            'numero': item['infNFe']['ide']['nNF'],
            'tipo': item['infNFe']['ide']['tpEmis'],
            'codigo': item['infNFe']['ide']['cNF'],
        }        
        chave = ChaveNFe(**vals)
        item['infNFe']['Id'] = gerar_chave(chave, 'NFe') 
    
    

def _send(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')

    xml = render_xml(path, '%s.xml' % method, **kwargs)

    pfx_path = certificado.save_pfx()
    signer = Assinatura(pfx_path, certificado.password)
    xml_signed = signer.assina_xml(xml, kwargs['NFes'][0]['infNFe']['Id'])

    url = localizar_url(0,  'RS')
    cabecalho = _build_header(**kwargs)

    return executar_consulta(certificado, url, cabecalho, xml_signed)


def autorizar_nfe(certificado, **kwargs):  # Assinar
    _generate_nfe_id(**kwargs)
    _send(certificado, 'NfeAutorizacao', **kwargs)


def retorno_autorizar_nfe(certificado, **kwargs):
    _send(certificado, 'NfeRetAutorizacao', **kwargs)


def recepcao_evento_cancelamento(certificado, **kwargs):  # Assinar
    _send(certificado, 'RecepcaoEventoCancelamento', **kwargs)


def inutilizar_nfe(certificado, **kwargs):  # Assinar
    _send(certificado, 'NfeInutilizacao', **kwargs)


def consultar_protocolo_nfe(certificado, **kwargs):
    _send(certificado, 'NfeConsultaProtocolo', **kwargs)


def nfe_status_servico(certificado, **kwargs):
    _send(certificado, 'NfeStatusServico.', **kwargs)


def consulta_cadastro(certificado, **kwargs):
    _send(certificado, 'NfeConsultaCadastro.', **kwargs)


def recepcao_evento_carta_correcao(certificado, **kwargs):  # Assinar
    _send(certificado, 'RecepcaoEventoCarta.', **kwargs)


def recepcao_evento_manifesto(certificado, **kwargs):  # Assinar
    _send(certificado, 'RecepcaoEventoManifesto', **kwargs)


def recepcao_evento_epec(certificado, **kwargs):  # Assinar
    _send(certificado, 'RecepcaoEventoEPEC', **kwargs)


def consulta_nfe_destinada(certificado, **kwargs):
    _send(certificado, 'NfeConsultaDest', **kwargs)


def download_nfe(certificado, **kwargs):
    _send(certificado, 'NfeDownloadNF', **kwargs)
