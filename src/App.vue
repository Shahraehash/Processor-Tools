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
};
</script>
