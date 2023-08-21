import React, { useState } from 'react';
import { StyleSheet, Text, View, Button, Image, TextInput, ScrollView } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

export default function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [response1, setResponse1] = useState('');
  const [response2, setResponse2] = useState('');
  const [result, setResult] = useState('');
  const [responseText, setResponseText] = useState('');
  const [confValues, setConfValues] = useState('');
  const [userInfo, setUserInfo] = useState({
    name: '',
    surname: '',
    age: '',
    height: '',
    shoeSize: '',
    dominantFoot: '',
    model1Result: '',
  });


  const pickImage = async (modelName) => {
    let result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
      base64: true,
    });

    if (!result.canceled) {
      setSelectedImage(result.uri);
      if (modelName === 'predict_ic') {
        sendImage(result.base64, modelName, setResponse1);
      } else if (modelName === 'predict_arka') {
        sendImage(result.base64, modelName, setResponse2);
      }
    }
  };

  const sendImage = async (base64Image, modelName, setResponse) => {
    try {
      const response = await axios.post(`http://192.168.0.12:8000/api/${modelName}`, {
        image: base64Image,
      });
      console.log(response.data);
      setResponse(response.data);
      var uzunluk = response.data.length;
      console.log("Dizinin uzunluğu: " + uzunluk);
    } catch (error) {
      console.error(error);
    }
  };
  
  const calculateSum = () => {
    const sum=Number(response1[7]) + Number(response2[49]) + Number(userInfo.model1Result);
   
   console.log(response2.key1)
    const conf2 = response2[63] + response2[64] + response2[65] + response2[66]
    const conf3 = response2[80] + response2[81] + response2[82] + response2[83]
    const conf4 = response2[97] + response2[98] + response2[99] + response2[100]
    const conf5 = response1[20] + response1[21] + response1[22] + response1[23]
    const conf6 = response2[114] + response2[115] + response2[116] + response2[117] 

    setResponseText(`Sum: ${sum}`);
    setConfValues(`Malleolar Curvature : ${conf2}\nCalcaneal frontal plane : ${conf3}\nBulging of the talonavicular joint: ${conf4}\nmedial longitudinal arch: ${conf5}\nAbduction/ adduction: ${conf6}`);

    let resultText = '';
    if (sum >= -12 && sum <= -5) {
      resultText = 'Highly Supinated';
    } else if (sum >= -4 && sum <= -1) {
      resultText = 'Supinated';
    } else if (sum >= 0 && sum <= 5) {
      resultText = 'Normal';
    } else if (sum >= 6 && sum <= 9) {
      resultText = 'Pronated';
    } else if (sum >= 10 && sum <= 14) {
      resultText = 'Highly Pronated';
    }

    setResult(resultText);
  };

  const handleInputChange = (field, value) => {
    setUserInfo({ ...userInfo, [field]: value });
  };

  return (
    <ScrollView contentContainerStyle={[styles.container, { paddingBottom: 32 }]}>
      <Text style={styles.title}>FPI-Foot Posture Index</Text>
      <Text style={styles.textLabel}>Name and Surname:</Text>
      <View style={styles.nameSurnameContainer}>
        <TextInput
          style={[styles.input, styles.halfInput]}
          onChangeText={(text) => handleInputChange('name', text)}
          value={userInfo.name}
        />
        <TextInput
          style={[styles.input, styles.halfInput]}
          onChangeText={(text) => handleInputChange('surname', text)}
          value={userInfo.surname}
        />
      </View>
      <Text style={styles.textLabel}>Age and Height:</Text>
      <View style={styles.ageHeightContainer}>
        <TextInput
          style={[styles.input, styles.halfInput]}
          onChangeText={(text) => handleInputChange('age', text)}
          value={userInfo.age}
        />
        <TextInput
          style={[styles.input, styles.halfInput]}
          onChangeText={(text) => handleInputChange('height', text)}
          value={userInfo.height}
        />
      </View>
      <Text style={styles.textLabel}>Shoe Size and Dominant Foot:</Text>
      <View style={styles.shoeFootContainer}>
        <TextInput
          style={[styles.input, styles.halfInput]}
          onChangeText={(text) => handleInputChange('shoeSize', text)}
          value={userInfo.shoeSize}
        />
        <TextInput
          style={[styles.input, styles.halfInput]}
          onChangeText={(text) => handleInputChange('dominantFoot', text)}
          value={userInfo.dominantFoot}
        />
      </View>
      <Text style={styles.textLabel}>Talar Head Palpation:</Text>
      <TextInput
        style={styles.input}
        onChangeText={(text) => handleInputChange('model1Result', text)}
        value={userInfo.model1Result}
      />
      <View style={styles.imageContainer}>
        {selectedImage && <Image source={{ uri: selectedImage }} style={styles.image} />}
      </View>
      <View style={styles.buttonContainer}>
        <Button title="Inside Photo" onPress={() => pickImage('predict_ic')} />
        <Button title="Backside Photo" onPress={() => pickImage('predict_arka')} />
      </View>
      <Button title="Calculate Sum" onPress={calculateSum} />
      <Text style={styles.responseText}>{responseText}</Text>
      <Text style={styles.responseText}>{result}</Text>
      <Text style={styles.responseText}>{confValues}</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    alignItems: 'center',
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 25,
  },
  textLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    alignSelf: 'flex-start',
    marginBottom: 8,
  },
  input: {
    width: '100%',
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 8,
    padding: 8,
  },
  imageContainer: {
    width: '100%',
    height: 200,
    marginBottom: 16,
  },
  image: {
    width: '100%',
    height: '100%',
    resizeMode: 'contain',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    marginBottom: 16,
  },
  responseText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 16,
  },
  table: {
    borderWidth: 1,
    borderColor: 'black',
    marginBottom: 16,
  },
  tableRow: {
    flexDirection: 'row',
  },
  footButtonsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  tableHeaderCell: {
    flex: 1,
    fontWeight: 'bold',
    paddingVertical: 8,
    paddingHorizontal: 4,
    borderWidth: 1,
    borderColor: 'black',
  },
  tableCell: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 4,
    borderWidth: 1,
    borderColor: 'black',
  },
  tableSeparator: {
    height: 4,
    backgroundColor: 'black',
    marginVertical: 8,
  },
  inputContainer: {
    marginBottom: 16,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  inputWrapper: {
    flex: 1,
    marginRight: 8,
  },
  nameSurnameContainer: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  ageHeightContainer: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  shoeFootContainer: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  halfInput: {
    flex: 1,
    marginRight: 4,
  },  
  cameraContainer: {
    position: 'relative',
    width: '100%',
    height: 300,
  },
  overlayContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

