def encode(a:int):
    b = 0
    Loop from 0 to value of a - 1 else exit
        var c ptr = b
        Loop from c/b to value of a -1 else b += 1
            d= c[0]
            e = c[0+1]
            e = d ^ e
            c[0+1] = e
            c = c + 1


        
    Label B_a(exit function)