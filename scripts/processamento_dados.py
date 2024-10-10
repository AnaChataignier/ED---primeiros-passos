import csv
import json


class Dados:
    
    def __init__(self, path, type_data):
        self.path = path
        self.type_data = type_data
        self.dados = self.leitura_dados()
        self.columns = self.get_columns()
        self.len_data = self.size_data() 
        
    def leitura_json(self):
        dados_json = []
        with open(self.path, 'r') as file:
            dados_json = json.load(file)
        return dados_json
    
    def leitura_csv(self):
        dados_csv = []
        with open(self.path, 'r') as file:
            spamreader = csv.DictReader(file, delimiter=',')
            for row in spamreader:
                dados_csv.append(row)
        return dados_csv      

    def leitura_dados(self):
        if self.type_data == 'csv':
            dados = self.leitura_csv()
        elif self.type_data == 'json':
            dados = self.leitura_json()
        elif self.type_data == 'list':
            dados = self.path  
            self.path = 'Lista processada na memória'
        return dados

    def get_columns(self):
        return list(self.dados[-1].keys())
            
    def rename_columns(self, key_mapping):
        new_dados = []

        for old_dict in self.dados:
            dict_temp = {}
            for old_key, value in old_dict.items():
                dict_temp[key_mapping[old_key]] = value
            new_dados.append(dict_temp)
            
        self.dados = new_dados
        self.columns = self.get_columns()

    def size_data(self):
        return len(self.dados)

    def join(dadosA, dadosB):
        combined_list = []
        combined_list.extend(dadosA.dados)
        combined_list.extend(dadosB.dados)
        return Dados(combined_list, 'list')

    def transform_data_table(self):
        dados_combinados_tabela = [self.columns]
        
        for row in self.dados:
            linha = []
            for coluna in self.columns:
                linha.append(row.get(coluna, 'Indisponivel'))
            dados_combinados_tabela.append(linha)
        return dados_combinados_tabela
        
    def save_data(self, path):
        dados_combinados_tabela = self.transform_data_table()
        with open(path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(dados_combinados_tabela)