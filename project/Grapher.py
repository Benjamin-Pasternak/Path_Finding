import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

objects = ('Forward_A*', 'Backwards_A*', 'Adaptive_A*')
y_pos = np.arange(len(objects))
performance = [3.88208e-09, 1.0138263999999999e-07 , 3.88208e-09]

plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.yticks([0.0, 3.8e-09, 1.1e-07], rotation = 20)
plt.xticks(y_pos, objects)
plt.xlabel('Time')
plt.title('Average Memory Taken Program Execution Large G')

for x,y in zip(y_pos,performance):

    label = str(y)

    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,3), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center



plt.show()



