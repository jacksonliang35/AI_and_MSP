import matplotlib.pyplot as plt
import matplotlib.animation as anim

fig = plt.figure()
ims = []
for add in range(20):
    im = plt.plot([0.5+add/50],[0.5+add/50],'ro',[1,1],[0.8-0.4+add/100,1-0.4+add/100],linewidth=5.0)
    ims.append(im)
im_ani = anim.ArtistAnimation(fig, ims, interval=50, repeat_delay=3000, blit=True)
plt.axis([0,1,0,1])
plt.show()
im_ani.save('./test.mp4')
