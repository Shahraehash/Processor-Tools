export default {
    data() {
      return {
        mxfileTypes: [
          {text: 'Training/Initial Test', value: 'train'},
          {text: 'Generalized Test', value: 'test'},
          {text: 'Train/Test Combined', value: 'combined'},
        ],

      };
    },
    created() {

    },
    methods: {
        mxfileTypeColor(fileType) {
            let color = null
            switch (fileType) {
              case 'train':
                color = '#2196F3'
                break;
              case 'test':
                color = '#9C27B0'
                break;
              case 'combined':
                color = '#FFC107'
                break;
              default:
                color = 'grey'
                break;
            }
            return color
      }
    }
  };