import cv2
import numpy as np
import math

VIEW_W, VIEW_H = 640, 480
FOV_DEG = 90
fov = math.radians(FOV_DEG)
def getEquirectangularVideo(path="360DegreeVideo/Zoo1.mp4"):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("Error: Could not open video file")
    else:
        print("Video file opened successfully")
    return cap

def buildRays(view_w,view_h,fov):
    aspect = view_w/view_h
    xs = (2*(np.arange(view_w) + .5)/view_w - 1)*aspect*math.tan(fov/2)
    ys = (1-2*(np.arange(view_h)+.5)/view_h)*math.tan(fov/2)
    xv,yv = np.meshgrid(xs,ys)
    zv = np.ones_like(xv)
    rays = np.stack([xv,yv,zv],axis=-1)
    rays /= np.linalg.norm(rays,axis=-1,keepdims=True)
    return rays.astype(np.float32)

def rotation_matrix(yaw,pitch):
    cy, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)
    Ry = np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])
    Rx = np.array([[1,0,0],[0,cp,-sp],[0,sp,cp]])
    return Ry @ Rx

def raysToEquirect(rays, W, H):
    x, y, z = rays[...,0], rays[...,1], rays[...,2]
    lat = np.arcsin(np.clip(y,-1,1))
    lon = np.arctan2(z,x)
    u = (lon+math.pi)/(2*math.pi)
    v =.5-lat/math.pi
    return (u*W).astype(np.float32), (v*H).astype(np.float32)

def readFrame(cap):
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        return None
    return frame

def main():
    step = 0.5
    yaw,pitch = 0,0
    cap = getEquirectangularVideo()
    
    if not cap.isOpened():
        print("Failed to open video. Exiting.")
        return
    
    rays = buildRays(VIEW_W,VIEW_H,fov)
    while True:
        frame = readFrame(cap)
        if frame is None:
            print("Error: Could not restart video. Exiting.")
            break

        key = cv2.waitKey(1) & 0xFF
        if key == ord('w'):
            pitch -= step
        elif key == ord('s'):
            pitch += step
        elif key == ord('a'):
            yaw -= step
        elif key == ord('d'):
            yaw += step
        elif key == 27:
            break
        
        R = rotation_matrix(yaw,pitch)
        rotatedRays = rays @ R.T

        H,W = frame.shape[:2]
        mapX,mapY = raysToEquirect(rotatedRays,W,H)

        view = cv2.remap(frame, mapX, mapY, interpolation=cv2.INTER_LINEAR)
        cv2.imshow("View",view)
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
    