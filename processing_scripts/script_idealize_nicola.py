from __future__ import division
import numpy as np

def idealize(root, subj):
    fs=256
    head=8
    dirs_in=["EKG256/", "EMG256/", "GSR256/", "TRIGGER256/", "TT256/"]
    files_in=["EKG","EMG", "GSR","TRIG"]    #TT a parte
    suffix="_"+subj+".txt"
    tt="TT_"+subj[:-2]+".txt"

    columns_out=["TIME","EKG", "EMG","GSR","TRIG", "LAB"]

    data_out=np.array([])

    for i in range(len(files_in)):
        fname=root+dirs_in[i]+files_in[i]+suffix
        data_in=np.genfromtxt(fname, skip_header=head, delimiter=",")
        new_cols=data_in[:,1]
        if new_cols.shape[0]<data_out.shape[0]:
            print "Reducing data_out by %d" % (-new_cols.shape[0]+data_out.shape[0])
            data_out=data_out[:new_cols.shape[0],:]
        elif new_cols.shape[0]>data_out.shape[0] and data_out.shape[0]!=0:
            print "Reducing new_cols by %d" % (new_cols.shape[0]-data_out.shape[0])
            new_cols=new_cols[:data_out.shape[0]]
        if data_out.shape[0]!=0:
            data_out=np.column_stack((data_out, new_cols))
        else:
            data_out=new_cols

    t = np.arange(len(data_out))/fs
    data_out=np.column_stack((t, data_out))

    data_TT =np.genfromtxt(root+dirs_in[4]+tt, skip_header=head, delimiter=",")[:,1]

    data_TT = (data_TT - np.min(data_TT))/(np.max(data_TT) - np.min(data_TT))

    start_first_video = np.where(data_TT>0.5)[0][0]
    intro = t[start_first_video]
    t_video_1 = 238 + 5
    t_video_2 = 240 + 5
    t_video_3 = 240 + 5
    t_video_4 = 242 + 5
    t_video_5 = 240 + 5
    t_video_6 = 243 + 5
    pause = 65

    timeline_periods = [0, intro, t_video_1, pause, t_video_2, pause, t_video_3, pause, t_video_4, pause, t_video_5, pause, t_video_6]
    timeline_classes = [0,1,0,2,0,3,0,4,0,5,0,6,0]
    timeline_times = np.cumsum(timeline_periods)
    timeline_times = np.r_[timeline_times, t[-1]]

    label_col = np.zeros(len(t))
    for i in range(len(timeline_times)-1):
        label_col[np.where((t>=timeline_times[i]) & (t<timeline_times[i+1]))[0]] = timeline_classes[i]

    data_out = np.column_stack((data_out, label_col))

    np.savetxt(subj+".csv", data_out, delimiter=",", header=",".join(columns_out), comments="", fmt="%0.6f")
switch=raw_input("Do you want to process one file at a time (o) or every file (e)? (o/e) ")=="o"
if switch:
    root=raw_input("Root dir (F/U/L): ")
    if root[-1]!="/":
        root+="/"
    subj=raw_input("Subject (ex F01_M): ")
    idealize(root, subj)
else:
    root=raw_input("Root dir (where you can find F, U and L folders): ")
    if root[-1]!="/":
        root+="/"
    msg="Number of patients in "
    types={"F":int(raw_input(msg+"F: ")), "L":int(raw_input(msg+"L: ")), "U":int(raw_input(msg+"U: "))}
    for type, n in types.items():
        for i in range(1, n+1):
            if i>=10:
                i=str(i)
            else:
                i="0"+str(i)

            for sex in ["M", "F"]:
                try:
                    print root+type+"/",type+i+"_"+sex
                    idealize(root+type+"/", type+i+"_"+sex)
                except IOError as e:
                    print "#ILLY"