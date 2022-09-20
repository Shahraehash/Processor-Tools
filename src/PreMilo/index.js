//https://www.loginradius.com/blog/engineering/write-a-javascript-library-using-webpack-and-babel/


import axios from 'axios'

let name = 'PreMilo';


const storeFile = async (file) => {
    var formData = new FormData();
    formData.append('files', file);

    const response = await axios.post('/preprocessor_api/integrated/store', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data //returns key value pair with file name and storage key
}




let FileObject = async (file) => {
    return {
        file,
        name: file.name,
        size: file.size,
        type: file.type,
        processing: false,
        evaluate: (analysis) => {analysis},
        process: (analysis) => {analysis},
    }
}



let transformOptions = [
    'seed',
    'split',
    'impute',
    'colinearity',
    'featureSelection',
    //'merge'
]

transformOptions

const createTransform = (action, analyze, transform) => {
    return {
        action,
        files: [],
        analyze,
        analysis: [],
        transform,
        
        options: {},

    }
}



import pmAssess from './pmSeed';

export default { 
    name, 
    storeFile,
    createTransform,
    FileObject,
    pmAssess 
}