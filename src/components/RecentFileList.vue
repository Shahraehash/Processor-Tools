<template>
  <div>
    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
          @click="query()"
          :loading="loading"
        >
          Dropdown
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          hover
          v-for="(file, key) in files" :key="key"
          @click="$emit('loadFile', file)"

        >Test
          <v-list-item-title>{{file.file_name}}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

  </div>

</template>
<script>
import CustObjs from '@/CustomObjects.js'

export default {
  name: 'RecentFileList',
  data() {
    return {
      loading: false,
      files: []

    }


  },
  methods: {
    query() {
      this.loading = true
      CustObjs.queryFileList().then(response => {
        this.files = response.data.reverse()
        this.loading = false
      })
    }
  }
}
</script>
