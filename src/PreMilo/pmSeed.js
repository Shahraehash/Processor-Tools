import {createTransform} from './index.js';

const storeFile = () => {
    console.log(createTransform('seed', 'analyze', 'transform'));
}

export default {
    storeFile
}