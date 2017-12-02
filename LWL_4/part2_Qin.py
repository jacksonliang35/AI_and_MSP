class pong:
    def __init__(self,x=0.5,y=0.5,vx=0.03,vy=0.01,py=0.5):
        self.ball_x = x
        self.ball_y = y #position
        self.velocity_x = vx
        self.velocity_y = vy #velocity
        self.paddle_y = py #paddle position
        return

    def printstate(self):
    	idx = np.zeros((12,12))#12*12 grid
    	img = []
    	for i in range(idx.shape[0]):
    		img.append([])
    		for j in range(idx.shape[1]):
    			if idx[i,j]==1:
    				img[i].append("a") # if have paddle or ball print
    			else:
    				img[i].append(" ") #background
    		img[i].append("\n")
        for line in img:
            print(''.join(line))
        return
