import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.IntegerSerializer;
import org.apache.kafka.common.serialization.StringSerializer;
import java.util.Arrays;
import KinectPV2.*;
import java.util.Properties;


KinectPV2 kinect;
PrintWriter output;
PrintWriter handpos;
color red = color(255,0,0);
color blue = color(0,0,255);


void setup() {
  size(1024, 848, P3D);

  kinect = new KinectPV2(this);
  kinect.enableDepthImg(true);
  kinect.enableSkeletonDepthMap(true);
  kinect.enableSkeleton3DMap(true);
  kinect.enableDepthMaskImg(true);
  kinect.init();
  output = createWriter("rawData.txt");
  handpos = createWriter("handPosition.txt");

}


int counter=0;
String name = "a";
PImage cap;
PImage depthmap;
ArrayList<KSkeleton> skeletonArray;
void draw() {
  counter++;
  background(0);

  //obtain the depth frame, 8 bit gray scale format
  depthmap = kinect.getDepthImage();
  cap = kinect.getDepthMaskImage();
  image(cap, 0, 0);

  skeletonArray =  kinect.getSkeletonDepthMap();
  //individual joints
  for (int i = 0; i < skeletonArray.size(); i++) {
    KSkeleton skeleton = (KSkeleton) skeletonArray.get(i);
    //if the skeleton is being tracked compute the skleton joints
    if (skeleton.isTracked()) {
      KJoint[] joints = skeleton.getJoints();

      color col  = skeleton.getIndexColor();
      fill(col);
      stroke(col);

      drawBody(joints);

    }
  }
  
  stroke(255);
  text(frameRate, 50, height - 50);
}



KJoint[] recordSkeleton3d()
{
    KSkeleton skeleton = (KSkeleton) kinect.getSkeleton3d().get(0);
    KJoint[] joints = skeleton.getJoints();
    return joints;
      
}

KJoint[] recordSkeleton2d()
{
    KSkeleton skeleton = (KSkeleton) kinect.getSkeletonDepthMap().get(0);
    KJoint[] joints = skeleton.getJoints();
    return joints;
}


void keyPressed()
{
  KJoint[] joints3d = recordSkeleton3d();
  KJoint[] joints2d = recordSkeleton2d();
  if(key=='a')
  {
    writeCloud(joints3d, joints2d,'a');
  }
}

void writeCloud(KJoint[] joints3d, KJoint[] joints2d,char k)
{
  //3d hand position print to console
  println("3d-position: ");
  println(joints3d[KinectPV2.JointType_HandLeft].getX());
  println(joints3d[KinectPV2.JointType_HandLeft].getY());
  println(joints3d[KinectPV2.JointType_HandLeft].getZ());
  //2d hand position saved to file
  handpos.print(joints2d[KinectPV2.JointType_HandLeft].getX() + ", ");
  handpos.print(joints2d[KinectPV2.JointType_HandLeft].getY() + ", ");
  handpos.print(joints3d[KinectPV2.JointType_HandLeft].getZ());
  handpos.println();
  handpos.flush();
  //save raw data to file
  int [] rawData = kinect.getRawDepthData();
  String strArray[] = new String[rawData.length];
  for (int i = 0; i < rawData.length; i++){
    strArray[i] = String.valueOf(rawData[i]);
  }
  String data = Arrays.toString(strArray);
  System.out.println(data.length());
  for(int i=0;i<rawData.length;i++)
  {
    output.print(rawData[i]);
    output.print(", ");
  }
  try{
    runProducer(data);
    //System.out.println(data);
  }catch(Exception e){
    System.out.println(e);
  }
  output.println();
  output.flush();
}


void drawBody(KJoint[] joints) {
  drawJoint(joints, KinectPV2.JointType_HandLeft, red);
}

void drawJoint(KJoint[] joints, int jointType, color tar) {
  pushMatrix();
  translate(joints[jointType].getX(), joints[jointType].getY(), joints[jointType].getZ());
  fill(tar);
  ellipse(0, 0, 25, 25);
  popMatrix();
}

private final static String TOPIC = "helloin2";
private final static String BOOTSTRAP_SERVERS = "18.217.86.48:9092";
private static Producer<String, String> createProducer() {
    Properties props = new Properties();
    props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
    props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,StringSerializer.class.getName());
    props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,StringSerializer.class.getName());
    props.put(ProducerConfig.MAX_REQUEST_SIZE_CONFIG, "9999999");
    return new KafkaProducer<String, String>(props);
}

static void runProducer(String data) throws Exception {
  Producer<String, String> producer = createProducer();
  
  String message = "{\"name\": \"" + "sdfgsdf" + "\"}";
  ProducerRecord<String, String> rec = new ProducerRecord<String, String>(TOPIC,"001",message);
  producer.send(rec).get();
}

    