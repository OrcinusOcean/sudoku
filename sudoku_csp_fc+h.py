import numpy as np
#import matplotlib.pyplot as plt
class Sudoku():
    step_threshold = 10000
    step_cunt = 0
    domains = range(1,10)
    stack = []

    def __init__(self, file_name):
        self.grid = []
        f = open(file_name, "r")
        f_lines = f.readlines()
        #read data
        for i in range(9):
            info = [int(i) for i in f_lines[i].split()]
            self.grid.append(info)
        self.update_var_table()
            #city_info.append([int(info[1]), int(info[2])]
    
    #if we assign that domain to the variable, return how many domains will reduce.
    def var_constraining_num(self, coord_x, coord_y, num=0):
        cunt = 0
        for i in range(9):
            if num == self.grid[coord_x][i]:
                cunt += 1
            if num == self.grid[i][coord_y]:
                cunt += 1
            cunt -= 2
        x_bound = 0
        y_bound = 0
        for i in range(3):
            if coord_x >= x_bound+i*3 and coord_x <= x_bound+i*3+2:
                x_bound = x_bound+i*3 
                for j in range(3):
                    if coord_y >= y_bound+j*3 and coord_y <= y_bound+j*3+2:
                        y_bound=y_bound+j*3
                        #print(x_bound)
                        #print(y_bound)
                        for i_bound in range(3):
                            for j_bound in range(3):
                                if self.grid[x_bound+i_bound][y_bound+j_bound] == num:
                                    cunt += 1
        cunt -= 1
        return cunt

    #update the remainning domains of each variable
    def update_var_table(self):
        self.var_table = []
        for i in range(9):
            var_line = []
            for j in range(9):
                if self.grid[i][j] == 0:
                    remain = [d for d in self.domains if self.is_assigniable(i, j, d)]  
                    var_line.append( {"domain":remain} )
                else:
                    var_line.append(-1)
            self.var_table.append(var_line)
        #print(np.matrix(self.var_table))

    #check if there is a variable has no domain
    def is_any_var_empty(self):
        for i in self.var_table:
            for j in i:
                if j != -1 and j['domain'] == []:
                    return True
        return False
    

    def display(self):
        print(np.matrix(self.grid))

    #check weather we can assign the domain to the variable
    def is_assigniable(self, coord_x, coord_y, num):
        for i in range(9):
            if num == self.grid[coord_x][i]:
                return False
            if num == self.grid[i][coord_y]:
                return False
        x_bound = 0
        y_bound = 0
        for i in range(3):
            if coord_x >= x_bound+i*3 and coord_x <= x_bound+i*3+2:
                x_bound = x_bound+i*3 
                for j in range(3):
                    if coord_y >= y_bound+j*3 and coord_y <= y_bound+j*3+2:
                        y_bound=y_bound+j*3
                        #print(x_bound)
                        #print(y_bound)
                        for i_bound in range(3):
                            for j_bound in range(3):
                                if self.grid[x_bound+i_bound][y_bound+j_bound] == num:
                                    return False
                        
        return True

    #return the indexs of the next blank
    def next_empty_grid(self):
        for x in range(9):
            for y in range(9):
                if(self.grid[x][y] == 0):
                    return x,y
        return -1,-1

    #choose most constrained variable and use most constraining variable to break tier
    def next_var(self): 
        x, y = self.next_empty_grid()
        if x == -1:
            return x, y
        x_m = x
        y_m = y
        for x in range(9):
            for y in range(9):
                if self.var_table[x][y] != -1:
                    if len(self.var_table[x][y]["domain"]) <= len(self.var_table[x_m][y_m]["domain"]) :
                        #use constraining variable method to break tier
                        if len(self.var_table[x][y]["domain"]) == len(self.var_table[x_m][y_m]["domain"]) :
                            if self.var_constraining_num(x, y) > self.var_constraining_num(x_m, y_m):
                                x_m = x
                                y_m = y
                        else:
                            x_m = x
                            y_m = y
        return x_m, y_m
                
    #Start our search
    def search(self):
        x, y = self.next_var()
        if x!= -1:
            available_d = [d for d in self.domains if self.is_assigniable(x, y, d)]
            var_constraining_num_list = [[d, self.var_constraining_num(x, y, d)] for d in available_d] 
            vcn_list_len = len(var_constraining_num_list)
            for i in range(vcn_list_len):
                    max_vcn = var_constraining_num_list[0]
                    for vcn in var_constraining_num_list:
                        if vcn[1] > max_vcn[1]:
                            max_vcn = vcn[1]
                    self.stack.append([[x, y, max_vcn[0] ]]) 
                    var_constraining_num_list.remove(max_vcn)
        while self.stack:
            action_cur = self.stack.pop()
            #print("*********************")
            #print(self.stack)
            #print(action_cur)
            #print("*********************")
            for a in action_cur:
                self.grid[a[0]][a[1]] = a[2]
            if action_cur != []:
                self.step_cunt += 1
                if self.step_cunt > self.step_threshold:
                    return False 
            self.update_var_table()
            x, y = self.next_var()
            #print(x, y)
            if x == -1:
                break
            available_d = [d for d in self.domains if self.is_assigniable(x, y, d)]
            if available_d == [] or self.is_any_var_empty():
                #print("empty")
                for a in action_cur:
                    self.grid[a[0]][a[1]] = 0
            else:
                #least-constraining value method
                #push the domain that redueces the biggest number of other variables'domain to the stack first
                #So that domain reduce smallest number of domains of other varibale can be assign first
                var_constraining_num_list = [[d, self.var_constraining_num(x, y, d)] for d in available_d] 
                vcn_list_len = len(var_constraining_num_list)
                for i in range(vcn_list_len):
                    max_vcn = var_constraining_num_list[0]
                    for vcn in var_constraining_num_list:
                        if vcn[1] > max_vcn[1]:
                            max_vcn = vcn[1]
                    action_new = action_cur.copy()
                    action_new.append([x, y, max_vcn[0]])
                    var_constraining_num_list.remove(max_vcn)
                    self.stack.append(action_new) 
        return True
            #self.display()


if __name__ == "__main__":
    y_list = []
    for j in range(1, 72):
        average_y = 0
        cunt_y = 0
        for i in range(1,11):
            input_file = "./"+str(j)+"/"+str(i)+".sd"
            sudoku = Sudoku(input_file)
            print("Input:")
            print("Input file is %s" % input_file)
            sudoku.display()
            if sudoku.search():
                print("result:")
                sudoku.display()
                average_y += sudoku.step_cunt
                cunt_y += 1
            else:
                print("Not solvable")
                sudoku.display()
            print("step count %s"% sudoku.step_cunt)
        average_y /= cunt_y
        y_list.append(average_y)
    print(y_list)
