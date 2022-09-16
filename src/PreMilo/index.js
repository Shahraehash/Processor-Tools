//https://www.loginradius.com/blog/engineering/write-a-javascript-library-using-webpack-and-babel/

let name = 'PreMilo';
let steps = [] // storage array of object steps

let apiBaseURL = '/premilo/';

let transformOptions = [
    'seed',
    'split',
    'impute',
    'colinearity',
    'featureSelection',
    //'merge'
]

const createTransform = (name, analyze, transform) => {
    return {
        action,
        files: [],
        analyze: (x => x),
        analysis: [],
        transform: (x => x),
        
        options: {},

    }
}

const queryBackend = (url, files, options) => {
    
    files.forEach(file => {
        // send file to backend
        // get response
        // store response
    })

    return fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json());
}


import pmAssess from './pmSeed';

export default { 
    name, 
    createTransform,
    pmAssess 
}