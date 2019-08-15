import graphics as g

WIDTH = 500
HEIGHT = 500


def distanceBetween(point1, point2):
    deltaPoint = g.Point(point1.x - point2.x, point1.y - point2.y)
    from math import sqrt
    return sqrt((deltaPoint.x ** 2) + (deltaPoint.y ** 2))


def drawEverything(win, points, lines):
    for p in points:
        p.undraw()
        p.draw(win)

    for l in lines:
        l.undraw()
        l.draw(win)


points1 = []
lines1 = []

points2 = []
lines2 = []

shapeDone = False
window = g.GraphWin("Window", WIDTH, HEIGHT)
while not shapeDone:
    recentPoint = window.getMouse()

    if len(points1) > 2:
        if distanceBetween(recentPoint, points1[0]) <= 10:
            lines1.append(g.Line(recentPoint, points1[0]))
            shapeDone = True
            drawEverything(window, points1, lines1)
            break

    if not shapeDone:
        points1.append(recentPoint)

    if len(points1) >= 2:
        p1 = points1[-2]
        p2 = points1[-1]
        lines1.append(g.Line(p1, p2))

    drawEverything(window, points1, lines1)

shapeDone = False

while not shapeDone:
    recentPoint = window.getMouse()

    for point in points2:
        if distanceBetween(recentPoint, g.Point(point[0], point[1])) <= 10:
            points2.append((points2[0][0], points2[0][1]))
            shapeDone = True
            break

    if not shapeDone:
        points2.append((recentPoint.x, recentPoint.y))

    if len(points1) >= 2:
        p1 = g.Point(points2[len(points2) - 2][0],
                     points2[len(points2) - 2][1])
        p2 = g.Point(points2[len(points2) - 1][0],
                     points2[len(points2) - 1][1])
        lines2.append(g.Line(p1, p2))

    drawEverything(window, [g.Point(x, y) for (x, y) in points2], lines2)
