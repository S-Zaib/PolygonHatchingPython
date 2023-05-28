import turtle
import os
import math

run = True
while(run):
    # create turtle object
    t = turtle.Turtle()

    # initialize empty list to store vertices, hole vertices
    vertices = []
    hole_vertices = [] 
    hatch_angle, spacing, offset = 0, 0, 0
    # set up turtle window
    turtle.setup(width=600, height=600)
    turtle.setworldcoordinates(-300, -300, 300, 300)
    t.speed(0)
    #prompt user for file mode or input mode
    mode = input("Enter 'f' for file mode or 'i' for input mode: ")

    # file mode
    if mode == 'f':
        # show all files in the directory and make the user choose
        print("Files in the directory:")
        for file in os.listdir():
            print(file)
    
        filename = input("Enter the name of the file: ")
        
        #first line has hatch angle and spacing
        with open(filename, 'r') as f:
            line = f.readline()
            hatch_angle, spacing, offset = line.split()
            hatch_angle = float(hatch_angle)
            spacing = float(spacing)
            offset = float(offset)
            t.penup()
            hole = False
            # read the vertices
            for line in f:
                if(line == 'hole\n'):
                    t.goto(vertices[0])
                    t.penup()
                    hole = True
                    continue
                x, y = line.split()
                if(hole):
                    hole_vertices.append((int(x), int(y)))
                else:
                    vertices.append((int(x), int(y)))
                t.goto(int(x), int(y))
                t.pendown()
                t.dot(5)
        # connect last vertex to first vertex to close the polygon
        if(len(hole_vertices) == 0):
            t.goto(vertices[0])
            t.penup()
        else:
            t.goto(hole_vertices[0])
            t.penup()

    # input mode
    elif mode == 'i':
        # prompt user for number of sides
        num_sides = int(input("Enter the number of sides for the polygon: "))
        # prompt user for vertices
        t.penup()
        for i in range(num_sides):
            x = int(input("Enter x-coordinate for vertex " + str(i+1) + ": "))
            y = int(input("Enter y-coordinate for vertex " + str(i+1) + ": "))
            vertices.append((x,y))
            t.goto(x, y)
            t.pendown()
            t.dot(5)
            # connect last vertex to first vertex to close the polygon
            if i == num_sides - 1:
                t.goto(vertices[0])
        # prompt user for hatch angle
        hatch_angle = float(input("Enter the angle for the hatch lines (in degrees) Recommended(110, 120, >180): "))
        spacing = float(input("Enter the spacing for the hatch lines (in mm): "))
        offset = float(input("Enter the offset for the hatch lines (0 for none): "))
        # prompt user for number of holes
        num_holes = int(input("Enter the number of holes (0 for none): "))
        # prompt user for hole vertices
        for i in range(num_holes):
            # prompt user for sides of hole
            t.penup()
            num_hole_sides = int(input("Enter the number of sides for hole " + str(i+1) + ": "))
            # prompt user for vertices
            for j in range(num_hole_sides):
                x = int(input("Enter x-coordinate for vertex " + str(j+1) + ": "))
                y = int(input("Enter y-coordinate for vertex " + str(j+1) + ": "))
                hole_vertices.append((x,y))
                t.goto(x, y)
                t.pendown()
                t.dot(5)
                # connect last vertex to first vertex to close the polygon
                if j == num_hole_sides - 1:
                    t.goto(hole_vertices[0])
        #promt user to save info to a file
        save = input("Would you like to save this information to a file? (y/n): ")
        if save == 'y':
            filename = input("Enter the name of the file: ") + '.txt'
            with open(filename, 'w') as f:
                f.write(str(hatch_angle) + ' ' + str(spacing) + ' ' + str(offset) + '\n')
                for vertex in vertices:
                    f.write(str(vertex[0]) + ' ' + str(vertex[1]) + '\n')
                f.write('hole\n')
                for vertex in hole_vertices:
                    f.write(str(vertex[0]) + ' ' + str(vertex[1]) + '\n')


    # function to calculate intersection point of two lines
    def line_intersection(line1, line2):
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if (denom == 0):
            return None

        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

        return (px, py)
    # function to check if a point is on a line segment
    def is_on_segment(p, line):
        x1, y1 = line[0]
        x2, y2 = line[1]
        px, py = p

        return (min(x1, x2) <= px <= max(x1, x2)) and (min(y1, y2) <= py <= max(y1, y2))

    # function to draw hatch lines
    def draw_hatch_lines(angle, hatch_spacing, vertices, tool_radius = 10):
        hatch_length = 1000
    
        def sort_key(p):
            x, y = p
            return (x - hatch_start[0]) ** 2 + (y - hatch_start[1]) ** 2
    
        def line_sort_key(line):
            x1, y1 = line[0]
            x2, y2 = line[1]
            return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
    
        def get_min_x(v):
            return v[0]
    
        def get_min_y(v):
            return v[1]
    
        # Calculate the bounding box of the original polygon
        min_x = min(vertices, key=get_min_x)[0]
        max_x = max(vertices, key=get_min_x)[0]
        min_y = min(vertices, key=get_min_y)[1]
        max_y = max(vertices, key=get_min_y)[1]

        # Create an offset polygon
        offset_vertices = []
        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i+1)%len(vertices)]
        
            # Calculate the angle of the line segment
            angle_rad = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        
            # Calculate the offset point for p1
            offset_p1 = (p1[0] + tool_radius*math.sin(angle_rad), p1[1] - tool_radius*math.cos(angle_rad))
            offset_vertices.append(offset_p1)
        
            # Calculate the offset point for p2
            offset_p2 = (p2[0] + tool_radius*math.sin(angle_rad), p2[1] - tool_radius*math.cos(angle_rad))
            offset_vertices.append(offset_p2)
    
        # Draw hatch lines
        diagonal_length = math.sqrt((max_x - min_x)**2 + (max_y - min_y)**2)
        hatch_start_x = min_x - diagonal_length * math.cos(math.radians(angle))
        hatch_start_y = min_y - diagonal_length * math.sin(math.radians(angle))
        hatch_end_x = max_x + diagonal_length * math.cos(math.radians(angle))
        hatch_end_y = max_y + diagonal_length * math.sin(math.radians(angle))

        for i in range(-int(diagonal_length / hatch_spacing) - 1, int(diagonal_length / hatch_spacing) + 2):
            hatch_start = (hatch_start_x + i * hatch_spacing * math.cos(math.radians(angle)),
                           hatch_start_y + i * hatch_spacing * math.sin(math.radians(angle)))
            hatch_end = (hatch_end_x + i * hatch_spacing * math.cos(math.radians(angle)),
                         hatch_end_y + i * hatch_spacing * math.sin(math.radians(angle)))

            intersections = []
            for j in range(len(offset_vertices)):
                line1 = (hatch_start, hatch_end)
                line2 = (offset_vertices[j], offset_vertices[(j + 1) % len(offset_vertices)])
                intersection = line_intersection(line1, line2)
                if intersection is not None and is_on_segment(intersection, line2):
                    intersections.append(intersection)

            intersections.sort(key=sort_key)

            sorted_lines = sorted([line for line in zip(intersections, intersections[1:])], key=line_sort_key)

            for line in sorted_lines:
                p1, p2 = line
                if math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) > hatch_length:
                    continue

                if math.sqrt((p1[0] - hatch_start[0])**2 + (p1[1] - hatch_start[1])**2) < tool_radius:
                    p1 = hatch_start
                if math.sqrt((p2[0] - hatch_end[0])**2 + (p2[1] - hatch_end[1])**2) < tool_radius:
                    p2 = hatch_end
            

                t.penup()
                t.goto(p1)
                t.pendown()
                t.goto(p2)

           

    # draw hatch lines
    color = "red"
    t.pencolor("red")

    draw_hatch_lines(hatch_angle, spacing, vertices, offset)
    t.pencolor("black")
    #fill vertices with colour white
    t.fillcolor("white")
    if len(hole_vertices) != 0:
        t.penup()
        t.goto(hole_vertices[0])
        t.begin_fill()
        for vertex in hole_vertices:
            t.pendown()
            t.goto(vertex)
        t.goto(hole_vertices[0])
        t.end_fill()


    #for i in range(0, 360, 10):
    #    print('Drawing for angle: ' + str(i) + ' degrees')
    #    draw_hatch_lines(i, spacing, vertices, 5)
    #    if color == "red":
    #        color = "blue"
    #    else:
    #        color = "red"
    #    t.pencolor(color)



    #ask user if they want to end program
    if input("End Program? (y/n)") == 'y':
        run = False

    turtle.clearscreen()

    ## keep window open
    #turtle.mainloop()




