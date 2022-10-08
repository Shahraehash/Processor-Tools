import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    //UI Component
    proLicense: false,
    snackbarMessage: {
      show: false,
      color: 'blue',
      message: 'Test message'
    },
    fileProcessingDialog: {
      loading: false,
      open: false
    },
    dataSet: [
      {name: 'Single File', value: 'combined'},
      {name: 'Training', value: 'training'},
      {name: 'Testing', value: 'testing'},
    ],
    tools: {
      'TrainTestSplit': {
        title: 'Train and Test Builder',
        icon: 'mdi-call-split',
        description: 'Build both a training and validation data set from a single data file.',
        isVisible: true,
        proLicense: false
      },
      'Colinearity': {
        title: 'Multicollinearity Assessment & Removal Tool',
        icon: 'mdi-chart-bell-curve-cumulative',
        description: 'Assess for multicollinearity in datasets along with feature removal options.',
        isVisible: true,
        proLicense: false
      },
      'FeatureSelector': {
        title: 'Feature Selector',
        icon: 'mdi-select-all',
        description: 'Select the subset of data with the most relative value.',
        isVisible: true,
        proLicense: false
      },
      'ColumnReducer': {
        title: 'Column Reducer Tool',
        icon: 'mdi-table-column-width',
        description: 'Extract specific columns from your training and test data to experiment with further refinement of your model.',
        isVisible: true,
        proLicense: false
      },
      'Encoder': {
        title: 'Imputation & Encoder Tool',
        icon: 'mdi-file-code-outline',
        description: 'Handle missing data and covert non-numeric datatypes.',
        isVisible: true,
        proLicense: true
      },
      'Integrated': {
        title: 'MERLIN',
        icon: 'mdi-bike-fast',
        description: 'Automatically select the appropriate steps to prepare your data for MILO.',
        isVisible: true,
        proLicense: true
      },      

    },
    diagnosticsEnabled: false
  },
  mutations: {
    //MessageSnackbar
    snackbarMessageSet(state, val) {
      state.snackbarMessage.show = true
      state.snackbarMessage.message = val.message
      state.snackbarMessage.color = val.color
    },
    //FileProcessingDialog
    FileProcessingDialogOpenSet(state, val) {
      state.fileProcessingDialog.open = val
    },
    FileProcessingDialogLoadingSet(state, val) {
      state.fileProcessingDialog.loading = val
    },
    setProLicense(state, val) {
      state.proLicense = val
    }
  },
  actions: {
  },
  modules: {
  }

})
