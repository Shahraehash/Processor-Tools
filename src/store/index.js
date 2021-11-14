import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    //UI Component
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
      {name: 'Training', value: 'training'},
      {name: 'Testing', value: 'testing'},
      {name: 'Combined Train/Test', value: 'combined_train_test'},
    ]
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
  },
  actions: {
  },
  modules: {
  }
})
