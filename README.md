# COVID-19-Surveillance-System

<h3><b>AI based Mask detection system to generate fine for public while driving</b></h3>

<h4>The problem</h4>

 As per WHO authorities, the two main routes of transmission of the COVID-19 virus are respiratory droplets and contact. Any person who is  in close contact (within 1 m) with someone who has respiratory symptoms (coughing, sneezing) is at risk of being exposed to potentially  infective respiratory droplets. Studies of influenza, influenza-like illness, and human coronaviruses provide evidence that the use of a medical mask can prevent the spread of infectious droplets from an infected person to someone else.

Monitoring people for wearing mask is a huge task, and especially, for a country like India, where population is more than a billion! <b>Our problem is aimed at creating a way to spread awareness while monitoring people for wearing their masks.</b> 

### Solution to the Problem

Though, we can’t check on each and every person, but what we could do is to <b>maximize</b> the surveillance system as much as possible and one of the best way to improve the system is by <b>automating the system</b> as much as possible.
So, our idea is to use the <b>CCTV cameras</b> on <b>Traffic signals</b> to detect if a person driving two wheelers is <b>wearing a mask</b> or not, and if not, then we can first warn him to wear mask and if found again, then fine him using the <b>QR Code</b>, which has to be attached in each and every vehicle(and he would be fined if the QR Code is not attached to the vehicle). The QR code will be provided free of cost and contain a person’s <b>Name</b> and <b>Phone number</b>.
Now, comes the <b>question on the availability of CCTV cameras</b>. Highly populated cities are more prone to this problem, so, our main target would be these cities. Third Eye campaign in Chennai has installed <b>34,293</b> cameras to monitor the speed activities which can be deployed for our project as well. Bengaluru has also put <b>5000</b> surveillance cameras on the road. In the similar manner, highly populated cities have good quantity of cameras for surveillance, which could be used for this project.

<b>The main motive behind this is to prevent the contact from infective respiratory droplets.</b>

## Technologies Used

* **TensorFlow** 
* **Keras**
* **OpenCv**
* **Pickle**
* **Twilio**
* **Python**
* <b>All the above dependencies need to be installed in order to test the project.</b>

### Demo
* **Video Link can be found on :-**

## WorkFlow
* We have designed a Deep Learning Neural Network which will feed on real time video captured through cctv cameras installed at traffic signals placed in different part of the city. The algorithm was trained on custom made dataset and images from online
* The first step after obtaining images was to pre-process the image into a one-D array containing RGB values. The values obtained were pre processed and then sent for further computation.
* The model uses CNN as a deep learning neural network to obtain good accuracy in predicting if a person wearing a Mask. In this step the image is convoluted, pooled and fed into layers of neural network using 'Selu' activation function. Then Flattened, and then sent to fully connected layer and Output layer.
* The model then predicts probability of a person wearing a mask for each frame of video and if the person is found without a mask, his vehicle will be searched for QR code and then a Warning / Fine will be sent to him digitally.

## Contributing
Pull requests are welcome. For major changes, a pull request is expected.

## The Team
* [Sourav Jain](https://github.com/SouravJain01)
* [Ritik Garg](https://github.com/rooky1905)
