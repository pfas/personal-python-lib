from decimal import Decimal
import decimal
import math

""" 地区范围相关, 网格操作函数 """
RECT_LEFT_BOT = 0
RECT_RIGHT_TOP = 1
RECT_LEFT_TOP = 0
RECT_RIGHT_BOT = 1
X = 0
Y = 1

# 程序使用字符串形式存储经纬度
# 在计算时考虑精度可使用 decimal 计算


def point2str(point):
    """
    point: (x, y) -> 'x,y'
    """
    return ','.join([point[0], point[1]])


def rect_str(rect):
    """
    rect: [point1, point2] -> 'point1|point2'
    """
    return '|'.join([point2str(p) for p in rect])


def str_to_rect(s: str):
    """
    'point1|point2' -> [(point1, point2)]
    """
    rect = None
    try:
        points = s.split('|')
        rect = [tuple(p.split(',')) for p in points]
    except Exception as e:
        pass
    return rect


def range_width(top_bot_rect, w: str):
    """
    return width pixel points of rect if the width of pixel point is w
    """
    width_len = Decimal(top_bot_rect[RECT_RIGHT_TOP][X]) - Decimal(top_bot_rect[RECT_LEFT_BOT][X])
    width = width_len / Decimal(w)
    return str(width.quantize(Decimal('0')))


def range_height(top_bot_rect, h: str):
    """
    return height pixel points of rect if the height of pixel point is h
    """
    height_len = Decimal(top_bot_rect[RECT_RIGHT_TOP][Y]) - Decimal(top_bot_rect[RECT_LEFT_BOT][Y])
    height = height_len / Decimal(h)
    return str(height.quantize(Decimal('0')))


def bot_top_rect2top_bot_rect(bot_top_rect):
    """
    covert a bot_top_rect(left_bot_point, right_top_point) to top_bot_rect(left_top_point, right_bot_point)
    """
    top_bot_rect = [('0', '0'), ('0', '0')]

    top_x = bot_top_rect[RECT_LEFT_BOT][X]
    top_y = bot_top_rect[RECT_RIGHT_TOP][Y]
    bot_x = bot_top_rect[RECT_RIGHT_TOP][X]
    bot_y = bot_top_rect[RECT_LEFT_BOT][Y]

    top_bot_rect = [(top_x, top_y), (bot_x, bot_y)]
    return top_bot_rect


""" 坐标系转化 """
PI = 3.1415926535897932384626
ee = 0.00669342162296594323
a = 6378245.0


def float_str_precision(s: str, precision='0.000000'):
    s = Decimal(s)
    return str(s.quantize(Decimal(precision)))


def point_precision(point, precision='0.000000'):
    return (float_str_precision(point[0]), float_str_precision(point[1]))


def wgs84_to_gcj02(lng, lat):
    """
    convert wgs84 to gcj02 (gaode)
    """
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * PI)
    mglat = lat + dlat
    mglng = lng + dlng
    return [str(mglng), str(mglat)]


def gcj02_to_wgs84(lng, lat):
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * PI)
    mglat = lat + dlat
    mglng = lng + dlng
    return [str(lng * 2 - mglng), str(lat * 2 - mglat)]


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * PI) + 40.0 * math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * PI) + 320 * math.sin(lat * PI / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * PI) + 40.0 * math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * PI) + 300.0 * math.sin(lng / 30.0 * PI)) * 2.0 / 3.0
    return ret


def wgs84_rect_to_gcj02_rect(wgs84_rect):
    first_point = wgs84_to_gcj02(float(wgs84_rect[0][0]), float(wgs84_rect[0][1]))
    second_point = wgs84_to_gcj02(float(wgs84_rect[1][0]), float(wgs84_rect[1][1]))
    return [point_precision(first_point), point_precision(second_point)]



def map_to_grid_left_top(left_top_rect, grid_size, point):

    left_top = (Decimal(left_top_rect[0][0]), Decimal(left_top_rect[0][1]))

    lng = Decimal(point[0])
    lat = Decimal(point[1])

    lng_size = Decimal(grid_size[0])
    lat_size = Decimal(grid_size[1])

    lng_diff = lng - left_top[0]
    lat_diff = left_top[1] - lat

    w = lng_diff / lng_size
    h = lat_diff / lat_size

    w = w.quantize(Decimal('0'), rounding=decimal.ROUND_FLOOR)
    h = h.quantize(Decimal('0'), rounding=decimal.ROUND_FLOOR)

    lng = left_top[0] + lng_size*w
    lat = left_top[1] - lat_size*h

    return (str(lng), str(lat)) 


def cut_rect_grid(top_bot_rect, step=None):
    left_top = top_bot_rect[RECT_LEFT_TOP]
    right_bot = top_bot_rect[RECT_RIGHT_BOT]

    bot_lat = decimal.Decimal(right_bot[Y])
    left_lng = decimal.Decimal(left_top[X])
    top_lat = decimal.Decimal(left_top[Y])
    right_lng = decimal.Decimal(right_bot[X])

    lng_diff = decimal.Decimal(step[0])
    lat_diff = decimal.Decimal(step[1])

    end_x = right_lng
    end_y = bot_lat

    y = top_lat
    while y > end_y:
        x = left_lng
        while x < end_x:
            yield [(str(x), str(y)), (str(x + lng_diff), str(y - lat_diff))]
            x = x + lng_diff 
        y = y - lat_diff