import itertools as itr

def general_rule_set_1(tup): 
  """
  rule set for determining the next step in a collatz like sequence
  
  tup : a tuple of integers
  
  returns a tuple of integers the same length as tup that has been incremented in the sequence
  """
  
  mask = [x % 2 for x in tup]
  
  #if all values are even
  if sum(mask) == 0:
    new = [x // 2 for x in tup]
  #if there is at least 1 odd value
  else:
    new = [3*tup[i] + mask[i] for i in range(len(tup))]
  
  return tuple(new)

def run_cycle(start, rule=general_rule_set_1, steps=300):
  """
  looks for a cycle that originates from the starting point
  
  start : a tuple of integers
  
  rule : the update rule
  
  steps : (positive int) the maximum number of steps to check for convergence within
  
  returns a boolean that represents whether a cycle was found in the specified number
  of steps or not (true if a cycle was found and false if not)
  """
  curr = start
  #create a set for checking for cycles
  visited = {curr}
  
  for i in range(steps):
    curr = rule(curr)
    #print(curr)
    if curr in visited:
      return True
    visited.update({curr})
    
  return False

def points_to_scad(space, dimension=2, with_negatives=True, steps=300):
  """
  calculates the set of bounded points within the number of steps
  based on the update rule
  
  space : (positive int) the side length of the number of values to check
  
  dimension : (positive int) the dimension of the sequence to check
  
  steps : (positive int) the maximum number of steps to check for convergence within
  
  returns the points that are bounded based on the increrment rule in
  a string that satisfies the OpeSCAD list definition
  """
  
  bounded = []
  
  #go through the points in the strictly positive quadrant
  for tup in itr.product([q for q in range(space)], repeat=dimension):
    
    if run_cycle(tup, rule=general_rule_set_1, steps=steps):
      bounded.append(tup)
  
  #go through the points in the strictly negative quadrant  
  if with_negatives:
    for tup in itr.product([-q for q in range(space)], repeat=dimension):
      
      if run_cycle(tup, rule=general_rule_set_1, steps=steps):
        bounded.append(tup)    
  
  #format the dta string nicely
  string = "pts = ["
  for i in range(len(bounded)-1):
    string += str(list(bounded[i])) + ",\n"
  string += str(list(bounded[len(bounded)-1]))
  string += "];" + (10*"\n")
  
  return string

def write_files():
  """
  create the data file and write the converging points to it
  
  also create the viewing file to view the data
  
  both files are OpenSCAD files
  """
  size = 40
  dim = 3
  data = points_to_scad(size, dimension=dim, with_negatives=True, steps=2000)
  
  with open("./data.scad", "w") as data_file:
    data_file.write(data)
  
  del data  
  
  #a correction for choosing between a dimension of 2 or greater
  correction = 1 + int(dim >= 3)
  
  viewer = """\
  include<data.scad>;
  
  for(p = pts){{
  
  translate(p)
  color([abs(p[0])/{0}, 1 - abs(p[1])/{0}, abs(p[{1}])/{0}, .5])
  cube(size=1, center=true);
  
  }}
  """.format(size, correction)
  
  with open("./viewer.scad", "w") as viewing_file: 
    viewing_file.write(viewer)

if __name__ == "__main__":
  write_files()


