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


# Given a list of pairs, returns a list of all cluster pairs
def get_clusters(blocks):
    clusters = []
    block_items = set(blocks)
    while block_items:
        cluster = get_connected(block_items.pop(), set(), block_items, set())[0]
        clusters.append(list(cluster))
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
    if len(cluster) == 0:
        return True
    up, down, left, right = get_bounds(cluster)

    tl = (up, left)
    br = (down, right)

    return all(pair[0] >= tl[0] and pair[1] >= tl[1] and pair[0] <= br[0] and pair[1] <= br[1] \
        for pair in cluster) and len(cluster) == (down-up+1)*(right-left+1)


# Split the given cluster on <= of the given line coords on the given axis
# if axis: 0 = on row (y-axis), 1 = on column (x-axis)
def split_cluster(cluster, line, axis):
    cluster_a, cluster_b = [], []
    for pair in cluster:
        target = cluster_a if pair[axis] <= line else cluster_b
        target.append(pair)
    return cluster_a, cluster_b

    
def explore_split(cluster, bounds, axis):
    valid_clusters = []
    for line in range(*bounds):
        new_cluster_a, new_cluster_b = split_cluster(cluster, line, axis)
        new_clusters = [] + get_clusters(new_cluster_a) + get_clusters(new_cluster_b)
        #print(f'clusters:\n{[sorted(c) for c in new_clusters]}')
        if all(is_rect(c) for c in new_clusters):
            valid_clusters.append(new_clusters)
    return valid_clusters


def explore_splits(cluster):
    up, down, left, right = get_bounds(cluster)
    print(up, down, left, right)
    
    hcs = explore_split(cluster, (up, down), 0)
    vcs = explore_split(cluster, (left, right), 1)
    
    print(f'hcs: {hcs}\nvcs:{vcs}\nlen(hcs)={len(hcs)} - len(vcs)={len(vcs)}')



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
        cs = []
        if all(is_rect(c) for c in cs):
            return cs


if __name__ == '__main__':
    colorama.init()
    csv = read_file('map1.csv')
    width = len(csv[0])     # columns
    height = len(csv)       # rows
    
    ccsv = [[0 if item == -1 else 1 for item in row] for row in csv]  # 0/1 pairs
    icsv = [[(r, c) for c in range(width)] for r in range(height)]    # Coord pairs
    csvprint(icsv, ccsv)
    
    all_pairs = [(r, c) for r, c in itertools.product(range(height), range(width)) if (ccsv[r][c] == 1)]
    clusters = [sorted(c) for c in get_clusters(all_pairs)]

    #for cluster in clusters:
        #extract_rects(cluster)
    cluster = clusters[0]
    explore_splits(cluster)


'''
[(4,5), (4,6), (4,7), (5,5), (5,6), (5,7), (6,5), (6,6), (6,7)]
[(4,5), (4,6), (4,7)]
'''
