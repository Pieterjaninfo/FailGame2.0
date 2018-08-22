import csv
from pprint import pprint
import itertools
import colorama

TILE_SIZE = 64


def read_file(filepath):
    with open(filepath, 'r') as f:
        return [[int(item) for item in row] for row in list(csv.reader(f, delimiter=','))]


def csvprint(csv, colors=None):
    print('[', end='')
    for id, row in enumerate(csv):
        if id > 0:
            print(' ', end='')
        if id < len(csv) -1:
            if colors:
                print('[' + ' '.join(('\033[32m(%1d,%2d)\033[37m' if colors[item[0]][item[1]] == 1 else '(%1d,%2d)') % (item[0],item[1]) for item in row) + ']')
            else:
                print('[' + ', '.join(('\033[32m%2d\033[37m' if item == 1 else '%2d') % item for item in row) + ']')
        else:
            if colors:
                print('[' + ' '.join(('\033[32m(%1d,%2d)\033[37m' if colors[item[0]][item[1]] == 1 else '(%1d,%2d)') % (item[0],item[1]) for item in row) + ']]')
            else:
                print('[' + ', '.join(('\033[32m%2d\033[37m' if item == 1 else '%2d') % item for item in row) + ']]')


def get_collisions(initial_pair, pairs):
    return [pair for pair in pairs if abs(initial_pair[0] - pair[0]) + abs(initial_pair[1] - pair[1]) == 1]


def get_connected(pair, current_set, main_set, visited):
    visited.update({pair})
    neighbours = set(get_collisions(pair, main_set))
    current_set = current_set.union({pair}).union(neighbours)
    
    for neighbour in neighbours:
        if neighbour not in visited:
            c, v = get_connected(neighbour, current_set, main_set, visited)
            current_set.update(c)
            visited.update(v)
    return current_set, visited


def get_clusters(csv):
    width = len(csv[0])
    height = len(csv)
    blocks = [(r, c) for r, c in itertools.product(range(height), range(width)) if (csv[r][c] == 1)]

    clusters = []
    block_items = set(blocks)
    while block_items:
        cluster = get_connected(block_items.pop(), set(), block_items, set())[0]
        clusters.append(cluster)
        block_items = block_items - cluster
    return clusters


def get_bounds(cluster):
    up    = min(cluster, key=lambda t: t[0])[0]
    down  = max(cluster, key=lambda t: t[0])[0]
    left  = min(cluster, key=lambda t: t[1])[1]
    right = max(cluster, key=lambda t: t[1])[1]
    return up, down, left, right


# Checks if a given rect is a cluster
def is_rect(cluster):
    up, down, left, right = get_bounds(cluster)

    tl = (up, left)
    br = (down, right)

    return all(pair[0] >= tl[0] and pair[1] >= tl[1] and pair[0] <= br[0] and pair[1] <= br[1] \
        for pair in cluster) and len(cluster) == (down-up+1)*(right-left+1)


def split_cluster(cluster):
    up, down, left, right = get_bounds(cluster)
    

# Requires: List of pairs of a cluster
def extract_rects(cluster):
    ipair = cluster[0]
    # Check if it's a simple straight line
    #if all(ipair[0] == pair[0] for pair in cluster) or all(ipair[1] == pair[1] for pair in cluster):
    #    return cluster
    if is_rect(cluster):
        print(cluster)
        return cluster
    else:
        print('cant find it yet')
        while True:





            if all(is_rect(c) for c in cs):
                return cs




if __name__ == '__main__':
    colorama.init()
    csv = read_file('map1.csv')
    ccsv = [[0 if item == -1 else 1 for item in row] for row in csv]
    icsv = [[(r, c) for c in range(len(csv[0]))] for r in range(len(csv))]
    csvprint(icsv, ccsv)

    clusters = [sorted(c) for c in get_clusters(ccsv)]
    
    for cluster in clusters:
        extract_rects(cluster)



'''
[(4,5), (4,6), (4,7), (5,5), (5,6), (5,7), (6,5), (6,6), (6,7)]
[(4,5), (4,6), (4,7)]
'''
