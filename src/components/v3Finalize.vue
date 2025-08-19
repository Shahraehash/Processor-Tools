<template>
    <div>
        <v3StepHeading
        style="display: inline-flex;"
        :stepNumber="stepNumber"
        :stepTitle="stepTitle"
        />

        <v-btn @click="$emit('removeComponent')" class="float-right" text v-if="optional" style="display: inline-flex;">
          Remove Step
          <v-icon >mdi-close</v-icon>
        </v-btn>  


        <div id="summary">
            <v-row dense wrap>
            <v-col cols="12">
                <div class="overline ml-4">Summary</div>
                <v-card outlined class="pa-3 ma-2">
                    <v3miniFilesDelta :originalArray="originalFiles" :finalArray="finalFiles"/>        
                </v-card>
            </v-col>
            <v-col cols="6">
                <div class="overline ml-4">Original File<span v-if="originalFiles.length > 1">s</span></div>
                <v-card outlined class="pa-3 ma-2" v-for="(original, originalKey) in originalFiles" :key="originalKey">
                    <v3miniFileInfo :fileInfo="original"/>
                </v-card>
                
                <!-- Target Column Encodings Section -->
                <div v-if="targetEncodings && targetEncodings.length > 0">
                    <div class="overline ml-4 mt-4">Target Column Encodings ({{ targetColumnName }})</div>
                    <v-card outlined class="pa-3 ma-2">
                        <div class="encoding-mappings">
                            <div v-for="(encoding, index) in targetEncodings" :key="index" class="encoding-row">
                                <span class="original-value">"{{ encoding.originalValue }}"</span>
                                <span class="arrow"> → </span>
                                <span class="encoded-value">{{ encoding.encodedValue }}</span>
                            </div>
                        </div>
                    </v-card>
                </div>
            </v-col>
            <v-col cols="6">
                <div class="overline ml-4">New Files to be Exported</div>
                <v-card outlined class="pa-3 ma-2" v-for="(current, currentKey) in finalFilesOnlyTrainTest" :key="currentKey">
                    <v3miniFileInfo :fileInfo="current"/>
                </v-card>
                
                <!-- Additional Audit Files moved to right column -->
                <div v-if="otherFiles.length > 0">
                    <div class="overline ml-4 mt-4">Additional Audit Files</div>
                    <v-card disabled="true" outlined class="pa-3 ma-2" v-for="(current, currentKey) in otherFiles" :key="currentKey">
                        <v3miniFileInfo :fileInfo="current"/>
                    </v-card>
                </div>             
            </v-col>                                    
        </v-row>

        </div>


        <!-- <v-text-field outlined label="Training File" style="display:inline-flex; width: 200px"></v-text-field>
        <v-text-field outlined label="Testing File" style="display:inline-flex; width: 200px"></v-text-field> -->
        




        
        <div class="text-right" v-if="files.length > 0">
            <v3ButtonNext 
            @next="exportFiles"
            text="Export Files"
        />

    </div>    
        
        <div v-if="analysis">

        </div>
    </div>
</template>
<script>
import v3StepHeading from '@/components/v3StepHeading'  
import FileDownload from 'js-file-download'
import JSZip from 'jszip'

import v3miniFilesDelta from '@/components/v3miniFilesDelta'
import v3miniFileInfo from './v3miniFileInfo.vue'
import v3ButtonNext from './v3ButtonNext.vue'
import { exportFileArray } from '@/v3Methods'



export default {
    name: 'v3Finalize',
    components: {
        v3StepHeading,
        v3miniFilesDelta,
        v3miniFileInfo,
        v3ButtonNext

    },
    props: {
        stepNumber: {
            type: Number || String
        },
        stepTitle: {
            type: String
        },
        optional: {
            type: Boolean,
            default: false
        },          
        files: {
            type: Array,
            default: () => []
        },        
        target: {
            type: String,
            default: null
        },
        analysis: {
            type: Object,
            default: () => {}
        },
        
    },
    data() {
        return {
            effect: null,
            loadedTargetEncodings: [],
        }
    },
    async mounted() {
        // Load target encodings from audit file when component mounts
        if (this.targetEncodingAuditFile) {
            this.loadedTargetEncodings = await this.getTargetEncodingsFromExportData()
        }
    },
    watch: {

    },
    computed: {
        originalFiles() {
            return this.files[0]
        },
        finalFiles() {
            return this.files[this.files.length - 1]
        },
        finalFilesOnlyTrainTest() {
            return this.finalFiles.filter(file => file.type === 'train' || file.type === 'test')
        },
        otherFiles() {
            return this.finalFiles.filter(file => file.type != 'train' && file.type != 'test')
        },
        targetEncodingAuditFile() {
            if (!this.finalFiles) return null
            return this.finalFiles.find(file => file.type === 'target_encoding_audit')
        },
        targetColumnName() {
            return this.target || 'target'
        },
        targetEncodings() {
            // Look for target mapping in the analysis data from File Validation step
            if (this.analysis && this.analysis.targetMap) {
                return Object.entries(this.analysis.targetMap).map(([originalValue, encodedValue]) => ({
                    originalValue,
                    encodedValue
                }))
            }
            
            // Fallback: Use loaded target encodings from audit file
            if (this.loadedTargetEncodings.length > 0) {
                return this.loadedTargetEncodings
            }
            
            return []
        },
        complete() {
            return true
        },        
    },
    methods: {
        async exportFiles() {
            this.$store.commit('FileProcessingDialogLoadingSet', true)
            this.$store.commit('FileProcessingDialogOpenSet', true)

            let fileObjects = await exportFileArray(this.files[this.files.length - 1])
            let zip = new JSZip()
            fileObjects.forEach(fileObj => {
                if (['train', 'test'].includes(fileObj.type) && fileObj.audit == false) {
                    zip.file(fileObj.name, fileObj.content)
                }
                else if (fileObj.audit == true) {
                    zip.folder('audit_files').file(`audit_${fileObj.name}`, fileObj.content)
                }
                
            })
            let file = await this.saveSummary()
            zip.file(file.name, file)
            let download = await zip.generateAsync({type:"blob"})
            
        
            //add 1 second automatic delay to UI
            const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
            await delay(1000);

            this.$store.commit('FileProcessingDialogLoadingSet', false)

            FileDownload(download, 'milo-ready-files.zip')
            
        },

        parseTargetEncodingsFromAuditFile() {
            // This method will be called during the export process when the audit file content is available
            // For now, return empty array as the content isn't directly accessible in the file metadata
            // The audit file content will be available during the exportFiles process
            return []
        },

        async getTargetEncodingsFromExportData() {
            // Get the audit file content from the export process
            try {
                let fileObjects = await exportFileArray(this.files[this.files.length - 1])
                const auditFile = fileObjects.find(file => file.type === 'target_encoding_audit')
                
                if (auditFile && auditFile.content) {
                    return this.parseCSVContent(auditFile.content)
                }
                
                return []
            } catch (error) {
                console.error('Error getting target encodings from export data:', error)
                return []
            }
        },

        parseCSVContent(csvContent) {
            try {
                const lines = csvContent.split('\n')
                const encodings = []
                
                // Skip header rows and separator row (first 3 lines)
                for (let i = 3; i < lines.length; i++) {
                    const line = lines[i].trim()
                    if (line) {
                        const columns = this.parseCSVLine(line)
                        if (columns.length >= 2 && columns[0] !== '---' && columns[0] !== '') {
                            encodings.push({
                                originalValue: columns[0],
                                encodedValue: columns[1]
                            })
                        }
                    }
                }
                
                return encodings
            } catch (error) {
                console.error('Error parsing CSV content:', error)
                return []
            }
        },

        parseCSVLine(line) {
            // Simple CSV parser for comma-separated values
            const result = []
            let current = ''
            let inQuotes = false
            
            for (let i = 0; i < line.length; i++) {
                const char = line[i]
                
                if (char === '"') {
                    inQuotes = !inQuotes
                } else if (char === ',' && !inQuotes) {
                    result.push(current.trim())
                    current = ''
                } else {
                    current += char
                }
            }
            
            result.push(current.trim())
            return result
        },

        async saveSummary() {
            const el = document.getElementById('summary')
              const options = {
                type: 'dataURL'
            }
            this.output = await this.$html2canvas(el, options);    
            return fetch(this.output).then(res => res.blob()).then(blob => {
                let file = new File([blob], 'summary.png', {type: 'image/png'})
                return file
                
            })

            
            
            

        }
            
    }
}
</script>
<style scoped>
.encoding-mappings {
    font-family: monospace;
    line-height: 1.6;
}

.encoding-row {
    display: flex;
    align-items: center;
    margin-bottom: 4px;
    padding: 2px 0;
}

.original-value {
    font-weight: 500;
    color: #1976d2;
    min-width: 120px;
    text-align: left;
}

.arrow {
    margin: 0 8px;
    color: #666;
    font-weight: bold;
}

.encoded-value {
    font-weight: 600;
    color: #388e3c;
    background-color: #f1f8e9;
    padding: 2px 6px;
    border-radius: 4px;
    min-width: 30px;
    text-align: center;
}
</style>
