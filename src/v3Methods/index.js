//https://www.loginradius.com/blog/engineering/write-a-javascript-library-using-webpack-and-babel/


import axios from 'axios'




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

//Validate files
let validateFiles = async (fileObjectArray, target)  => {

    let json = {fileObjectArray, target}
    const response = await axios.post('/preprocessor_api/integrated/validate', json, {
      headers: {
        'Content-Type': 'application/json',
      }
    })
    return response.data
}   



export { 
    storeFile,
    paramFile,
    storeParamFile,
    validateFiles

}