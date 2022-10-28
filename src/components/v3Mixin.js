
export default {
    data() {
      return {
        mxfileTypes: [
          {text: 'Only Training/Initial Test', value: 'train'},
          {text: 'Only Generalization Test', value: 'test'},
          {text: 'Combined Train/Generalization', value: 'combined'},
        ],

      };
    },
    created() {

    },
    methods: {
        mxStylePercent(value) {
          if (value < 1) {
            return '<1'
          }
          else {
            return Math.round(value)
          }

        },
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
                color = 'grey'
                break;
              default:
                color = 'grey'
                break;
            }
            return color
      },

    }
  };