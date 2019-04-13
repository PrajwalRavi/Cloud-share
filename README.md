# Facilitating sharing of data using blockchain.

By this project, we tried to implement the paper : [Blockchain-based Personal Health Data Sharing System Using Cloud Storage.](https://www.researchgate.net/publication/328906581_Blockchain-based_Personal_Health_Data_Sharing_System_Using_Cloud_Storage)

### Abstract 
With the advent of rapid development of wearable
technology and mobile computing, huge amount of personal
health-related data is being generated and accumulated on
continuous basis at every moment. This research work proposes a conceptual design for sharing personal continuous-
dynamic health data using blockchain technology supplemented
by cloud storage to share the health-related information in a
secure and transparent manner.

### Architecture 
* DynamoDb provided by Amazon AWS was used to store the data to be shared.
* Just the table name and a short description was stored in the blocks in the blockchain.

![architecture](https://github.com/PrajwalRavi/MiniSQL/blob/master/architecure.png)

### Future plans
* Integrate this into a web-app using Django, enabling user accounts etc.
* Try to implement the key-holder part of the architecture. 