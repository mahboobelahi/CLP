import random


def generateboxes(container, num):
    
    retry = 600 * num
    while num > 1:
        cuboid = random.choice(container)
        #cuboid = container[0]
        
        
        while cuboid[3] <= 39 or cuboid[4] <= 29 or cuboid[5] <= 19:
            retry -= 1
            if retry == 0:
                print("Cannot partition into packages. Please try again")
                return
            #container.remove(cuboid)
            cuboid = random.choice(container)
        container.remove(cuboid)
        prob = random.uniform(0, 1)
        x1 = cuboid[0]
        y1 = cuboid[1]
        z1 = cuboid[2]
        x2 = cuboid[3]
        y2 = cuboid[4]
        z2 = cuboid[5]
        if prob < 0.35:
            # Split in length
            t = random.randint(5, int(x2 / 2))
            package1 = [x1 + t, y1, z1, x2 - t, y2, z2]
            package2 = [x1, y1, z1, t, y2, z2]
        elif prob < 0.65:
            # Split in width
            t = random.randint(5, int(y2 / 2))
            package1 = [x1, y1 + t, z1, x2, y2 - t, z2]
            package2 = [x1, y1, z1, x2, t, z2]

        else:
            # Split in height
            t = random.randint(5, int(z2 / 2))
            package1 = [x1, y1, z1 + t, x2, y2, z2 - t]
            package2 = [x1, y1, z1, x2, y2, t]

        # package1.append((package1[3]*package1[4]*package1[5]))
        # package2.append((package2[3]*package2[4]*package2[5]))
        container.append(package1)
        container.append(package2)
        #container = sorted(container,  key=lambda x: x[-1],reverse=True)
        num -= 1

    return container
