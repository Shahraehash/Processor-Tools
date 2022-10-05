//https://www.loginradius.com/blog/engineering/write-a-javascript-library-using-webpack-and-babel/


import axios from 'axios'


let buildTransformObject =  (method, data) => {
  return {method, data}
}

let fileTypeColor = (fileType) => {
  let color = null
  switch (fileType) {
    case 'traing':
      color = 'green'
      break;
    case 'test':
      color = 'blue'
      break;
    case 'combined':
      color = 'red'
      break;
    default:
      color = 'grey'
      break;
  }
  return color
}


//Store file in backend and generate ID
let storeFile = async (file) => {
    var formData = new FormData();
    formData.append('files', file);

    const response = await axios.post('/preprocessor_api/integrated/store', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data //returns key value pair with file name and storage key
}

//Calculate file parameters
let paramFile = async (json) => {
    const response = await axios.post('/preprocessor_api/integrated/params', json, {
        headers: {
          'Content-Type': 'application/json',
        }
      })
      return response.data
}

//Store and calculate parameters together
let storeParamFile = async (file) => {
    let response = await storeFile(file)
    let result = await paramFile(response)
    result['type'] = null
    return result
}


//ANALYSIS
let analyzeFileArray = async (fileObjectArray, target, analyze) => {
  let json = {fileObjectArray, target, analyze}
  console.log(json)
  const response = await axios.post('/preprocessor_api/integrated/analyze', json, {
    headers: {
      'Content-Type': 'application/json',
    }
  })
  return response.data  

}

//EFFECT
let effectFileArray = async (fileObjectArray, target, effect) => {
  let json = {fileObjectArray, target, effect}
  const response = await axios.post('/preprocessor_api/integrated/effect', json, {
    headers: {
      'Content-Type': 'application/json',
    }
  })  
  return response.data  
}

//TRANSFORM
let transformFileArray = async (fileObjectArray, target, transform) => {
  let json = {fileObjectArray, target, transform}
  const response = await axios.post('/preprocessor_api/integrated/transform', json, {
    headers: {
      'Content-Type': 'application/json',
    }
  })
  return response.data  
}


//EXPORT
let exportFileArray = async (fileObjectArray) => {
  let json = {fileObjectArray}
  const response = await axios.post('/preprocessor_api/integrated/export', json, {
    headers: {
      'Content-Type': 'application/json',
    }
  })
  return response.data  
}








export { 
    buildTransformObject,
    fileTypeColor,
    storeFile,
    paramFile,
    storeParamFile,
    transformFileArray,
    analyzeFileArray,
    effectFileArray,
    exportFileArray
    

}