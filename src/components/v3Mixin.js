
export default {
    data() {
      return {
        mxfileTypes: [
          {text: 'Training', value: 'train'},
          {text: 'Generalization Test', value: 'test'},
          {text: 'Combined Train/Test', value: 'combined'},
        ],
        mxBarColors: {
          train: '#2196F3',
          test: '#81C784',  //alts 1 and alts 2: 
          blank: 'grey', 
          classZero: '#9C27B0',
          classZeroLight: '#AB47BC',
          classOne: '#3F51B5',
          classOneLight: '#5C6BC0',
          missing: '#FFA726',

        }


      };
    },
    created() {

    },
    methods: {
      mxRoundValue(val) {
        return Math.round(val * 10) / 10;
      },

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
              color = this.mxBarColors.train
              break;
            case 'test':
              color = this.mxBarColors.test
              break;
            case 'combined':
              color = this.mxBarColors.blank
              break;
            default:
              color = this.mxBarColors.blank
              break;
          }
          return color
      },


    }
  };