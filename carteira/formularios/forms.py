from carteira.models import ContaUsuario
from django import forms


class Balanco(forms.Form):
        
    casa = ['Aluguel', 'Condomínio', 'Conta de água',
            'Conta de luz', 'Gás', 'Telefone', 'Internet',
            'IPTU', 'Financiamento', 'Outros - casa']

    lazer = ['Restaurantes', 'Bar', 'Cinema', 'Viagem',
                'Festas/Eventos', 'Presentes', 'Outros - Entretenimento']

    saude = ['Remédios', 'Convênio', 'Outros - Saúde']

    transp = ['IPVA', 'Combustível', 'Manutenção', 'Táxi',
                'Transporte público', 'Outros - Transporte']

    basico = ['Comida', 'Bebida', 'Produtos de limpeza',
                'Higiene pessoal', 'Outros - Necessidade']

    pessoais = ['Roupa', 'Maquiagem', 'Cosméticos', 'Outros - pessoal']

    filhos = ['Escola', 'Roupa - Filho', 'Brinquedo']

    outros = ['Cartão', 'Gastos Pessoais',
                'Investimento PMS', 'Investimento PMR', 'Investimento PI']

    categorias = {'Casa': casa, 'Lazer': lazer,
                            'Saúde': saude, 'Transporte': transp,
                            'Necessidade Básica': basico,
                            'Cuidados Pessoais': pessoais,
                            'Outros': outros,
                            'Maju': filhos}

    gastos_list = [gasto for key, gasto in categorias.items()]
    options = [e for lista in gastos_list for e in lista]
    options.append('---')
    options = tuple([(e,  e) for key, e in enumerate(options)])
    valor = forms.DecimalField(min_value=0, decimal_places=2, required=False, label='Valor R$')
    categoria = forms.ChoiceField(choices=options, initial='---', required=False)
    gasto_extra = forms.ChoiceField(choices=(('G', 'Gasto'), ('E', 'Extra')), label='Fonte', initial='Gasto')
    

