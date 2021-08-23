<template>
  <v-app>
    <v-main>
      <router-view/>
      <MessageSnackbar />
    </v-main>
  </v-app>
</template>

<script>
import MessageSnackbar from '@/components/MessageSnackbar.vue'

export default {
  name: 'App',
  components: {
    MessageSnackbar
  },

  data: () => ({
    //
  }),
};
</script>
