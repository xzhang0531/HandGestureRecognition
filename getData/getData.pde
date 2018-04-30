import org.apache.kafka.clients.producer.*;
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.serialization.IntegerSerializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.common.serialization.IntegerDeserializer;
import org.apache.kafka.common.serialization.StringDeserializer;
import java.util.Arrays;
import KinectPV2.*;
import java.util.Properties;
import java.util.Collections;

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
  output = createWriter("rawData_y.txt");
  handpos = createWriter("handPosition_y.txt");

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
  String handLocation = joints2d[KinectPV2.JointType_HandLeft].getX() + ", " + joints2d[KinectPV2.JointType_HandLeft].getY() + ", " + joints3d[KinectPV2.JointType_HandLeft].getZ();

  //save raw data to file
  int [] rawData = kinect.getRawDepthData();
  String strArray[] = new String[rawData.length];
  for (int i = 0; i < rawData.length; i++){
    strArray[i] = String.valueOf(rawData[i]);
  }
  String data = Arrays.toString(strArray);
  //System.out.println(data.length());
  for(int i=0;i<rawData.length;i++)
  {
    output.print(rawData[i]);
    output.print(", ");
  }
  try{
    runProducer(data, handLocation);
    //runConsumer();
    //System.out.println(handLocation);
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

private final static String TOPIC = "hgr-wf-in";
//private final static String TOPIC2 = "hgr-preprocess-out";
//private final static String TOPIC3 = "hgr-predict-in";
private final static String BOOTSTRAP_SERVERS = "18.217.86.48:9092";
private static Producer<String, String> createProducer() {
    Properties props = new Properties();
    props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
    props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,StringSerializer.class.getName());
    props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,StringSerializer.class.getName());
    props.put(ProducerConfig.MAX_REQUEST_SIZE_CONFIG, "9999999");
    return new KafkaProducer<String, String>(props);
}
//private static Consumer<String, String> createConsumer() {
//    Properties props = new Properties();
//    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
//    props.put(ConsumerConfig.GROUP_ID_CONFIG, "xiangyuzhang");
//    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
//    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,StringDeserializer.class.getName());
//    props.put(ConsumerConfig.MAX_PARTITION_FETCH_BYTES_CONFIG, "9999999");
//    final Consumer<String, String> consumer = new KafkaConsumer<String, String>(props);
//    consumer.subscribe(Collections.singletonList(TOPIC2));
//    return consumer;
//}

static void runProducer(String data, String handLocation) throws Exception {
  Producer<String, String> producer = createProducer();
  
  String message = "{\"rawData\": \"" + data + "\", \"handLocation\": \"" + handLocation + "\"}";
  //System.out.println(message);
  ProducerRecord<String, String> rec = new ProducerRecord<String, String>(TOPIC,"001",message);
  producer.send(rec).get();
}

//static void runConsumer() throws Exception {
//  Consumer<String, String> consumer = createConsumer();
//  final int giveUp = 100;   int noRecordsCount = 0;
//  while (true) {
//      //System.out.println(noRecordsCount);
//      final ConsumerRecords<String, String> consumerRecords = consumer.poll(20);

//      if (consumerRecords.count()==0) {
//          noRecordsCount++;
//          if (noRecordsCount > giveUp) break;
//          else continue;
//      }

//      for (ConsumerRecord<String, String> record : consumerRecords) {
//            Producer<String, String> producer = createProducer();

//            String message = record.value();
//            System.out.println(message);
//            ProducerRecord<String, String> rec = new ProducerRecord<String, String>(TOPIC3,"001",message);
//            producer.send(rec);
//            break;
//      }

//      consumer.commitAsync();

//  }
//  consumer.close();
//  System.out.println("DONE");
  
//}
    