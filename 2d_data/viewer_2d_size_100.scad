  include<data_2d_size_100_steps_2000.scad>;
  
  for(p = pts){
  
  translate(p)
  color([abs(p[0])/100, 1 - abs(p[1])/100, abs(p[ 1 ])/100, .5])
  cube(size=1, center=true);
  
  }
  