<template>
    <div class="text-right">
        <v-btn @click="exportFiles()" text icon x-large><v-icon>mdi-table-arrow-right</v-icon></v-btn>
    </div>
</template>
<script>    
import { exportFileArray } from '@/v3Methods'

import FileDownload from 'js-file-download'
import JSZip from 'jszip'

export default {
    name: 'v3miniValidate',
    props: {
        currentFiles: {
            type: Array,
            default: () => []
        },
    },
    methods: {
        async exportFiles() {
            let fileObjects = await exportFileArray(this.currentFiles)
            let zip = new JSZip()
            fileObjects.forEach(fileObj => {
                zip.file(fileObj.name, fileObj.content)
            })
            let download = await zip.generateAsync({type:"blob"})
            FileDownload(download, 'export.zip')
        }
    }
}
</script>
<style scoped>
.inline-div {
    display: inline;
}
</style>