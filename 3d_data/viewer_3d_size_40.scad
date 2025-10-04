  include<data_3d_size_40_steps_2000.scad>;
  
  for(p = pts){
  
  translate(p)
  color([abs(p[0])/40, 1 - abs(p[1])/40, abs(p[2])/40, .5])
  cube(size=1, center=true);
  
  }
  