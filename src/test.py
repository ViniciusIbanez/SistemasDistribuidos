from subprocess import check_output
from Naked.toolshed.shell import execute_rb, muterun_rb
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import datetime
import sys


# plt.use('Agg')


def retrieve_vns():
    #os.environ["file_name"] = input("Nome do arquivo:\n")
    t0 = time.time()
    success = execute_rb('vns.rb')
    t1 = time.time() - t0  ##Tempo que demora o ruby
    ref_arquivo = open("best.txt", 'r')
    cost = ref_arquivo.readline()
    best_txt = ref_arquivo.read()
    best_txt = best_txt.replace("[", "").replace("]", "")
    splitado = best_txt.split(", ")
    r = []
    for i in range(0, len(splitado)):
        r.append(int(splitado[i]))
    return r, cost, t1


def read_points():
    pontos = []
    conjunto_pontos = []
    ref_arquivo = open(os.getenv("file_name"), 'r')

    for linha in ref_arquivo:
        valores = linha.split()
        pontos = [int(valores[1]), int(valores[2])]
        conjunto_pontos.append(pontos)
    ref_arquivo.close()
    # retorno = f'\nConjunto pontos = {conjunto_pontos}'
    # print(retorno)
    # print(conjunto_pontos)
    return conjunto_pontos


def retrieve_points():
    vns_rout, cost, t1 = retrieve_vns()
    points_rout = read_points()
    points_to_draw = []
    for element in vns_rout:
        points_to_draw.append(points_rout[element])
    points_to_draw.append(points_rout[vns_rout[0]])
    # retorno = f'\nPoints to draw = {points_to_draw}'
    # print(retorno)
    log_file = open(f'out{os.getenv("file_name")}_{hex(hash(t1))}.txt', 'w')
    log_file.write(f'Custo = {cost}\nTempo = {t1} segundos\n')
    log_file.write(f'Caminho\n')
    for element in points_to_draw:
        log_file.write(f'{element}\n')
    log_file.write(f'EOF')
    log_file.close()
    return points_to_draw, cost, t1


# 9136
def define_map():
    array = read_points()
    ax = plt
    for i in range(len(array)):
        my_plotter(ax, array[i][0], array[i][1], {'marker': 'h'})
        ##ax.plot(array[i], array[i - 1])
    return ax


def my_plotter(ax, data1, data2, param_dict):
    out = ax.plot(data1, data2, **param_dict)
    return out


def draw_path(caminho, nome):
    plt = define_map()
    plt.title(nome)
    for i in range(0, len(caminho) - 1):
        plt.arrow(caminho[i][0], caminho[i][1],
                  caminho[i + 1][0] - caminho[i][0],
                  caminho[i + 1][1] - caminho[i][1],
                  width=0.00, head_length=0.0, head_width=0.0)
        #plt.pause(0.15)#faz o desenho ficar animado e bonito porém crasha o save.....
    # plt.axis('scaled')
    #fig = plt
    #fig.savefig(f'{os.getenv("file_name")}_{hex(hash(t1))}.png')
    plt.show()
    #plt.close()


##############################################################################################################
nomes = ['cases/dsj1000.tsp']
for name in nomes:
    print(f'Iniciando teste para: {name}')
    os.environ["file_name"] = name
    for i in range(1):
    ##    i += 1
        cost = 0
        points_to_draw = []
        points_to_draw, cost, t1 = retrieve_points()
        # print(points_to_draw)
        print('Custo = ' + str(cost))
        print('Tempo=' + str(float(t1) / 60) + ' minutos')
        draw_path(points_to_draw, str(os.getenv("file_name")) +
                  ' Custo ' + str(cost) +
                  '\nTempo=' + str(int(t1 / 60)) + ":" + str(int(t1 % 60)))

