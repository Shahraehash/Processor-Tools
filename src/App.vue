<template>
  <v-app>
    <v-main>
      <TopBar />
      <router-view/>
      <MessageSnackbar />
      <FileProcessingDialog
        :isOpen="$store.state.fileProcessingDialog.open"
        :loading="$store.state.fileProcessingDialog.loading"
      />
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios'

import TopBar from '@/components/TopBar.vue'
import MessageSnackbar from '@/components/MessageSnackbar.vue'
import FileProcessingDialog from '@/components/FileProcessingDialog.vue'

export default {
  name: 'App',
  components: {
    TopBar,
    MessageSnackbar,
    FileProcessingDialog
  },

  data: () => ({
    //
  }),
  mounted() {
    axios.get('/preprocessor_api/license').then(response => {
      try {
        if (
          response.headers['milo-education'] == 'false' &&
          response.headers['milo-trial'] == 'false'
        ) {
          this.$store.commit('setProLicense', true)
        }
        //defaults to false
      } catch(err) {
        this.$store.commit('setProLicense', false)
      }
    })
  }
};
</script>
