<template>
  <v-dialog max-width="700" v-model="dialogOpen">
    <v-card flat class="pa-3 pb-6">
      <v-card-title>
        <p>Import Columns from MILO Results "report.csv" File</p>
        <v-spacer></v-spacer>
        <v-btn @click="dialogOpen = false" icon class="mt-n5">
          <v-icon medium>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="mx-0 py-0">
        <v-file-input prepend-icon="mdi-file" chips truncate-length="200" outlined label="MILO Data File"  @change="fileUpload"></v-file-input>
        <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
        <v-spacer></v-spacer>
        <div>
          <div class="ml-8 mb-3" >Select columns based on the feature selector method. Note: Random Forest options are not included because each is run specific. Also, any method that does not reduced the number of columns is not included.</div>
          <v-select v-if="miloMetadata" :items="miloMetadata" v-model="columns" class="ml-8"  outlined  label="Feature Selector Method"></v-select>
          <div>
            <v-chip small color="grey lighten-2" v-for="(item, key) in columns" :key="key">{{item}}</v-chip>
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="mr-2" rounded dark color="primary" @click="setMiloColumns">Select Columns</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
//packages
import axios from 'axios'

//support code

//components

export default {
  name: 'MiloFileUploadDialog',
  components: {

  },
  props: [

  ],
  data() {
    return {
      dialogOpen: false,
      loading: false,
      miloMetadata: null,
      columns: []
    }
  },
  methods: {
    open() {
      this.dialogOpen = true
    },
    fileUpload(file){
      if (file != null) {
        var formData = new FormData();
        this.loading = true

        formData.append("file", file);
        axios.post('/preprocessor_api/shared/milo_report_file_upload', formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            'X-inbound': 'milo_file'
          }
        }).then(result => {
          this.miloMetadata = []
          let data = JSON.parse(result.data.result).selected_features
          for (let i in data) {
            this.miloMetadata.push({
              text: i,
              value: JSON.parse(data[i])
            })
          }
          this.loading = false
        })
      }
      else {
        this.miloMetadata = null
        this.loading = false
      }
    },
    setMiloColumns() {
      this.$emit('setMiloColumns', this.columns)
      this.dialogOpen = false
    }
  }
}
</script>
