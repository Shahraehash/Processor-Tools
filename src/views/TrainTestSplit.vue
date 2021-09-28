<template>
  <v-container>
    <v-card
      class="ma-3 pa-3"
      outlined
    >
      <div>
        <v-row>
          <v-col cols="3">
            <v-btn
              icon
              @click="$router.push({name: 'Landing'})"
            >
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
          </v-col>
          <v-col
            cols="6"
            class="text-center"
          >
            <v-icon x-large>mdi-call-split</v-icon>
            <span class="title">Train and Test Builder</span>
          </v-col>
          <v-col cols="3">
          </v-col>
        </v-row>
      </div>
      <v-card-text class="body-1">
        This tool allows you to build both a training and validation data set from a single data file.
      </v-card-text>
    </v-card>






    <!-- <v-stepper v-model="e1">
        <v-stepper-header>
          <v-stepper-step
            :complete="e1 > 1"
            step="1"
          >
            Select Data File
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step
            :complete="e1 > 2"
            step="2"
          >
            Select Target Column
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step
            :complete="e1 > 3"
            step="3"
          >
            Select Split
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step step="4">
            Output
          </v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step="1">

            <div class="text-right pa-2">
              <v-btn
                color="primary"
                @click="e1 = 2"
                :disabled="fileData == null"
              >
                Next
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </div>
          </v-stepper-content>

          <v-stepper-content step="2">
            <v-card
              class="ma-3 px-4 py-2"
              flat
            >

              <v-row>
                <v-col cols="6">
                  <v-select
                    clearable
                    outlined
                    label="Target Column"
                    prepend-icon="mdi-bullseye"
                    v-if="fileData"
                    v-model="targetColumn"
                    :items='fileData.column_names'
                    @change="determineClassMetadata"
                  ></v-select>
                </v-col>
              </v-row>
              <v-alert
                dense
                text
                type="info"
                v-if="class0nanSize >0 || class1nanSize > 0"
              >
                Some data cannot be used.
                <span v-if="class0nanSize >0">For class 0, {{class0nanSize}} row
                  <span v-if="class0nanSize == 1"> is </span>
                  <span v-if="class0nanSize > 1">s are </span>excluded.
                </span>
                <span v-if="class1nanSize >0">For class 1, {{class1nanSize}} row
                  <span v-if="class1nanSize == 1"> is </span>
                  <span v-if="class1nanSize > 1">s are </span>excluded.
                </span>


              </v-alert>
              <div style="width:100%" >
                <div
                  class="distrobution-box"
                  v-bind:style="{
                    background: '#2196F3',
                    width: class0percent + '%'
                    }"
                  >
                  <div
                    v-bind:style="{
                      opacity: 0.3,
                      background:'white',
                      width: class0nanPercent + '%',
                      position:'absolute',
                      left:'16px',
                      bottom:'15px'
                      }"
                    class="distrobution-box"
                  >
                  </div>
                  <p class="pa-0 ma-0">
                    Class 0 ({{class0percent}}%)
                  </p>
                  <p class="pa-0 ma-0" v-if="class0nanSize == 0">
                    N={{class0size}}
                  </p>
                  <p class="pa-0 ma-0" v-if="class0nanSize > 0">
                    <span style="text-decoration: line-through">{{class0size}}</span>
                    <v-icon color="white">mdi-arrow-right</v-icon>
                    {{class0size - class0nanSize}}
                  </p>
                </div>
                <div
                  class="distrobution-box"
                  v-bind:style="{
                    background: '#009688',
                    width: class1percent + '%'
                    }"
                  >
                  <div
                    v-bind:style="{
                      opacity: 0.3,
                      background:'white',
                      width: class1nanPercent + '%',
                      position:'absolute',
                      right:'16px',
                      bottom:'15px'
                      }"
                    class="distrobution-box"
                  >
                  </div>
                  <p class="pa-0 ma-0">
                    Class 1 ({{class1percent}}%)
                  </p>
                  <p class="pa-0 ma-0" v-if="class1nanSize == 0">
                    N={{class1size}}
                  </p>
                  <p class="pa-0 ma-0" v-if="class1nanSize > 0">
                    <span style="text-decoration: line-through">{{class1size}}</span>
                    <v-icon color="white">mdi-arrow-right</v-icon>
                    {{class1size - class1nanSize}}
                  </p>
                </div>

                <div class="distrobution-box" v-bind:style="{ background: '#d3d3d3', width: placeholderSlot + '%' }">Data Distrobution Displayed After Selection</div>
              </div>





              <v-alert
                v-if="minSampleSizeError"
                color="red"
                type="error"
              >To use this tool, each class must have a an N greater than {{minSampleSize}}.</v-alert>

            </v-card>


            <v-row class="pa-2">
              <v-col cols="6" class="text-left">
                <v-btn
                  class="mr-3"
                  text
                  @click="e1 = 1"
                >
                  <v-icon>mdi-chevron-left</v-icon>
                  Previous
                </v-btn>

              </v-col>
              <v-col cols="6" class="text-right">
                <v-btn
                  float="right"
                  color="primary"
                  @click="e1 = 3"
                  :disabled="!(!minSampleSizeError && targetColumn != null)"
                >
                  Next
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </v-col>
            </v-row>





          </v-stepper-content>

          <v-stepper-content step="3">
            <v-card
              class="ma-3 px-4 py-2"
              flat
              v-if="!minSampleSizeError && targetColumn != null"

            >
              <div >
                Select amount of training data. {{minSampleSize}} is the minimum supported sample size. We have automatically selected a value that you may adjust below.
              </div>
              <v-row>
                <v-col cols="5">
                  <v-slider
                    :min="minSampleSize"
                    :max="maxSampleSize"
                    v-model="trainingClassSampleSize"
                    @change="calculatePercentage"
                  ></v-slider>
                </v-col>
                <v-col cols="1">
                  {{trainingClassSampleSize}}
                </v-col>
              </v-row>
              <div >
                Select how you would like to use remain data in the global generalization testing set.
              </div>
              <v-radio-group v-model="prevalenceOption" @change="calculatePercentage">
                <v-radio label="Use All Remaining Data After Training Data Removed"></v-radio>
                <v-radio label="Maintain Original Prevalence in Validation File (some data will be removed)"></v-radio>
              </v-radio-group>

                <v-card flat class="mb-10">
                  <div style="width:100%">

                    <div
                      class="title-box"
                      v-bind:style="{
                        background: 'white',
                        width: barSizes.nan + '%'
                        }"
                      >
                    </div>


                    <div
                      class="title-box"
                      v-bind:style="{
                        background: '#7E57C2',
                        width: barSizes.train0 + barSizes.train1 + '%'
                        }"
                      >
                      Training Data
                    </div>
                    <div
                      class="title-box"
                      v-bind:style="{
                        background: '#5C6BC0',
                        width: barSizes.test0 + barSizes.test1 + '%'
                        }"
                      >
                      Generalization Testing Data
                    </div>
                  </div>
                  <div style="width:100%">

                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <div
                          class="distrobution-box"
                          v-bind="attrs"
                          v-on="on"
                          v-bind:style="{
                            background: 'grey',
                            width: barSizes.nan + '%'
                            }"
                          >
                          <div>n={{fileData.nan_count}}</div>
                        </div>

                      </template>
                      <span>{{fileData.nan_count}} rows are missing data and cannot be used in the final data set</span>
                    </v-tooltip>




                    <div
                      class="distrobution-box"
                      v-bind:style="{
                        background: '#64B5F6',
                        width: barSizes.train0 + '%'
                        }"
                      >
                      <div>Train 0</div>
                      <div>n={{trainingClassSampleSize}}</div>
                    </div>
                    <div
                      class="distrobution-box"
                      v-bind:style="{
                        background: '#4DB6AC',
                        width: barSizes.train1 + '%'
                        }"
                      >
                      <div>Train 1</div>
                      <div>n={{trainingClassSampleSize}}</div>
                    </div>
                    <div
                      class="distrobution-box"
                      v-bind:style="{
                        background: '#42A5F5',
                        width: barSizes.test0 + '%'
                        }"
                      >
                      <div>Test 0</div>
                      <div>n={{barData.test0global}}</div>
                    </div>
                    <div
                      class="distrobution-box"
                      v-bind:style="{
                        background: '#26A69A',
                        width: barSizes.test1 + '%'
                        }"
                      >
                      <div>Test 1</div>
                      <div>n={{barData.test1global}}</div>
                    </div>
                    <div
                      class="distrobution-box"
                      v-bind:style="{
                        background: '#F48FB1',
                        width: barSizes.extra + '%'
                        }"
                      >
                      <div>Not Used</div>
                      <div>n={{barData.extra}}</div>
                    </div>
                  </div>
                </v-card>
            </v-card>


            <v-row class="pa-2">
              <v-col cols="6" class="text-left">
                <v-btn
                  class="mr-3"
                  text
                  @click="e1 = 2"
                >
                  <v-icon>mdi-chevron-left</v-icon>
                  Previous
                </v-btn>

              </v-col>
              <v-col cols="6" class="text-right">
                <v-btn
                  dark
                  float="right"
                  color="primary"
                  @click="e1 = 4"
                >
                  Next
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-stepper-content>
          <v-stepper-content step="4">

            <div class="overline mb-5">Training and Testing Data File Outputs</div>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="outputFiles.training"
                  outlined
                  dense
                  label="Training Data File Name"
                  suffix=".csv"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="outputFiles.testing"
                  outlined
                  dense
                  label="Testing Data File Name"
                  suffix=".csv"
                ></v-text-field>
              </v-col>
            </v-row>

            <div v-if="e1 == 4">
              <div class="overline">Additional File Outputs</div>
              <v-row>
                <v-col cols="6"
                  v-if="prevalenceOption == 1"

                >

                  <v-switch
                  label="Export unused data from the majority class."
                  v-model="outputSettings.extraFile"
                  ></v-switch>

                  <v-text-field
                    outlined
                    dense
                    label="Extra Data File"
                    suffix=".csv"
                    v-model="outputFiles.extra"
                    v-if="outputSettings.extraFile"
                  ></v-text-field>
                </v-col>

                <v-col cols="6"

                  v-if="fileData.nan_count > 0"
                >
                  <div>
                    <v-switch
                    label="Export the rows missing data."
                    v-model="outputSettings.nanFile"
                    ></v-switch>
                  </div>
                  <v-text-field
                    outlined
                    dense
                    label="Rows with Missing Data File"
                    suffix=".csv"
                    v-model="outputFiles.nan"
                    v-if="outputSettings.nanFile"
                  ></v-text-field>
                </v-col>

              </v-row>

            </div>

            <v-row class="pa-2">
              <v-col cols="6" class="text-left">
                <v-btn
                  class="mr-3"
                  text
                  @click="e1 = 3"
                >
                  <v-icon>mdi-chevron-left</v-icon>
                  Previous
                </v-btn>

              </v-col>
              <v-col cols="6" class="text-right">
                <v-btn
                  dark
                  float="right"
                  color="primary"
                  @click="processFiles()"

                >
                  Create Files
                  <v-icon class="pl-2">mdi-file</v-icon>
                </v-btn>
              </v-col>
            </v-row>


          </v-stepper-content>
        </v-stepper-items>
      </v-stepper> -->




      <!-- STEP 1 -->
      <v-card

        outlined
        class="ma-3 pa-5"
      >
        <StepHeading
          stepNumber="1"
          stepTitle="Select Data File"
        />
        <div>
          <!-- Training -->
          <v-card outlined class="ma-5 pa-3">
            <div class="overline ml-5 mb-3">
              Single Data File
            </div>

            <v-layout class="ml-5">
              <v-row>
                <v-col cols="6" >

                  <v-file-input v-model="file" prepend-icon="mdi-file" chips truncate-length="100" outlined label="Training Data File"  @change="fileUpload"></v-file-input>
                </v-col>
                <v-col cols="6" class="text-center">
                  <v-progress-circular color="blue" size="50" width="10" v-if="fileDataLoading" indeterminate></v-progress-circular>
                  <DataValidation
                    class="mt-n3"
                    :fileData="fileData"
                    dataType="combined"
                    @dataValid="fileValidationData"
                  />
                </v-col>
              </v-row>
            </v-layout>
          </v-card>

          <ErrorMessage v-if="fileDataValid ? fileDataValid.errors.missingData : false" type="warning" text="Rows with missing data will be dropped during processing." />
          <ErrorMessage v-if="fileDataValid ? fileDataValid.errors.textData : false" type="error" text="Milo cannot use columns with non-numerical data. This must be fixed before the tool can proceed." />

        </div>
      </v-card>

      <!-- STEP 2 -->
      <v-card
        v-if="showStep2"
        outlined
        class="ma-3 pa-5"
      >
        <StepHeading
          stepNumber="2"
          stepTitle="Select Target Column"
        />
        <div>

          <v-row>
              <v-col cols="6">
                <v-select
                  clearable
                  outlined
                  label="Target Column"
                  prepend-icon="mdi-bullseye"
                  v-if="fileData"
                  v-model="targetColumn"
                  :items='fileData.column_names'
                  @change="determineClassMetadata"
                ></v-select>
              </v-col>
            </v-row>
            <v-alert
              dense
              text
              type="info"
              v-if="class0nanSize >0 || class1nanSize > 0"
            >
              Some data cannot be used.
              <span v-if="class0nanSize >0">For class 0, {{class0nanSize}} row
                <span v-if="class0nanSize == 1"> is </span>
                <span v-if="class0nanSize > 1">s are </span>excluded.
              </span>
              <span v-if="class1nanSize >0">For class 1, {{class1nanSize}} row
                <span v-if="class1nanSize == 1"> is </span>
                <span v-if="class1nanSize > 1">s are </span>excluded.
              </span>


            </v-alert>
            <div style="width:100%" >
              <div
                class="distrobution-box"
                v-bind:style="{
                  background: '#2196F3',
                  width: class0percent + '%'
                  }"
                >
                <div
                  v-bind:style="{
                    opacity: 0.3,
                    background:'white',
                    width: class0nanPercent + '%',
                    position:'absolute',
                    left:'16px',
                    bottom:'15px'
                    }"
                  class="distrobution-box"
                >
                </div>
                <p class="pa-0 ma-0">
                  Class 0 ({{class0percent}}%)
                </p>
                <p class="pa-0 ma-0" v-if="class0nanSize == 0">
                  N={{class0size}}
                </p>
                <p class="pa-0 ma-0" v-if="class0nanSize > 0">
                  <span style="text-decoration: line-through">{{class0size}}</span>
                  <v-icon color="white">mdi-arrow-right</v-icon>
                  {{class0size - class0nanSize}}
                </p>
              </div>
              <div
                class="distrobution-box"
                v-bind:style="{
                  background: '#009688',
                  width: class1percent + '%'
                  }"
                >
                <div
                  v-bind:style="{
                    opacity: 0.3,
                    background:'white',
                    width: class1nanPercent + '%',
                    position:'absolute',
                    right:'16px',
                    bottom:'15px'
                    }"
                  class="distrobution-box"
                >
                </div>
                <p class="pa-0 ma-0">
                  Class 1 ({{class1percent}}%)
                </p>
                <p class="pa-0 ma-0" v-if="class1nanSize == 0">
                  N={{class1size}}
                </p>
                <p class="pa-0 ma-0" v-if="class1nanSize > 0">
                  <span style="text-decoration: line-through">{{class1size}}</span>
                  <v-icon color="white">mdi-arrow-right</v-icon>
                  {{class1size - class1nanSize}}
                </p>
              </div>

              <div class="distrobution-box" v-bind:style="{ background: '#d3d3d3', width: placeholderSlot + '%' }">Data Distrobution Displayed After Selection</div>
            </div>
            <ErrorMessage
              v-if="minSampleSizeError"
              type="error"
              :text="'To use this tool, each class must have a an N greater than ' + minSampleSize "
              />



        </div>
      </v-card>

      <!-- STEP 3 -->
      <v-card
        outlined
        class="ma-3 pa-5"
        v-if="showStep3"
      >
        <StepHeading
          stepNumber="3"
          stepTitle="Select Split"
        />
        <div>

          <div>
            Select amount of training data. {{minSampleSize}} is the minimum supported sample size. We have automatically selected a value that you may adjust below.
          </div>
          <v-row>
            <v-col cols="5">
              <v-slider
                :min="minSampleSize"
                :max="maxSampleSize"
                v-model="trainingClassSampleSize"
                @change="calculatePercentage"
              ></v-slider>
            </v-col>
            <v-col cols="1">
              {{trainingClassSampleSize}}
            </v-col>
          </v-row>
          <div >
            Select how you would like to use remain data in the global generalization testing set.
          </div>
          <v-radio-group v-model="prevalenceOption" @change="calculatePercentage">
            <v-radio label="Use All Remaining Data After Training Data Removed"></v-radio>
            <v-radio label="Maintain Original Prevalence in Validation File (some data will be removed)"></v-radio>
          </v-radio-group>
          <v-card flat class="mb-10">
            <div style="width:100%">

              <div
                class="title-box"
                v-bind:style="{
                  background: 'white',
                  width: barSizes.nan + '%'
                  }"
                >
              </div>


              <div
                class="title-box"
                v-bind:style="{
                  background: '#7E57C2',
                  width: barSizes.train0 + barSizes.train1 + '%'
                  }"
                >
                Training Data
              </div>
              <div
                class="title-box"
                v-bind:style="{
                  background: '#5C6BC0',
                  width: barSizes.test0 + barSizes.test1 + '%'
                  }"
                >
                Generalization Testing Data
              </div>
            </div>
            <div style="width:100%">

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <div
                  class="distrobution-box"
                  v-bind="attrs"
                  v-on="on"
                  v-bind:style="{
                    background: 'grey',
                    width: barSizes.nan + '%'
                    }"
                  >
                  <div>n={{fileData.nan_count}}</div>
                </div>

              </template>
              <span>{{fileData.nan_count}} rows are missing data and cannot be used in the final data set</span>
            </v-tooltip>
            <div
              class="distrobution-box"
              v-bind:style="{
                background: '#64B5F6',
                width: barSizes.train0 + '%'
                }"
              >
              <div>Train 0</div>
              <div>n={{trainingClassSampleSize}}</div>
            </div>
            <div
              class="distrobution-box"
              v-bind:style="{
                background: '#4DB6AC',
                width: barSizes.train1 + '%'
                }"
              >
              <div>Train 1</div>
              <div>n={{trainingClassSampleSize}}</div>
            </div>
            <div
              class="distrobution-box"
              v-bind:style="{
                background: '#42A5F5',
                width: barSizes.test0 + '%'
                }"
              >
              <div>Test 0</div>
              <div>n={{barData.test0global}}</div>
            </div>
            <div
              class="distrobution-box"
              v-bind:style="{
                background: '#26A69A',
                width: barSizes.test1 + '%'
                }"
              >
              <div>Test 1</div>
              <div>n={{barData.test1global}}</div>
            </div>
            <div
              class="distrobution-box"
              v-bind:style="{
                background: '#F48FB1',
                width: barSizes.extra + '%'
                }"
              >
              <div>Not Used</div>
              <div>n={{barData.extra}}</div>
            </div>
          </div>
        </v-card>

        </div>
      </v-card>

      <!-- STEP 4 -->
      <v-card
        v-if="showStep4"
        outlined
        class="ma-3 pa-5"
      >
        <StepHeading
          stepNumber="4"
          stepTitle="Output Files"
        />
        <div>
          <div>

            <v-switch v-model="outputSettings.includeRowIndex" label="Include row index in output"></v-switch>
          </div>

          <v-row>
            <v-col cols="6">
              <v-text-field
                v-model="outputFiles.training"
                outlined
                dense
                label="Training Data File Name"
                suffix=".csv"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                v-model="outputFiles.testing"
                outlined
                dense
                label="Testing Data File Name"
                suffix=".csv"
              ></v-text-field>
            </v-col>
          </v-row>

          <div >
            <div class="overline">Additional File Outputs</div>
            <v-row>
              <v-col cols="6"
                v-if="prevalenceOption == 1"

              >

                <v-switch
                label="Export unused data from the majority class."
                v-model="outputSettings.extraFile"
                ></v-switch>

                <v-text-field
                  outlined
                  dense
                  label="Extra Data File"
                  suffix=".csv"
                  v-model="outputFiles.extra"
                  v-if="outputSettings.extraFile"
                ></v-text-field>
              </v-col>

              <v-col cols="6"

                v-if="fileData.nan_count > 0"
              >
                <div>
                  <v-switch
                  label="Export the rows missing data."
                  v-model="outputSettings.nanFile"
                  ></v-switch>
                </div>
                <v-text-field
                  outlined
                  dense
                  label="Rows with Missing Data File"
                  suffix=".csv"
                  v-model="outputFiles.nan"
                  v-if="outputSettings.nanFile"
                ></v-text-field>
              </v-col>

            </v-row>

          </div>
          <div class="text-right">
            <v-btn
              dark
              rounded
              float="right"
              color="primary"
              @click="processFiles()"
            >
              Create Files
              <v-icon class="pl-2">mdi-file</v-icon>
            </v-btn>

          </div>






        </div>
      </v-card>




      <v-dialog
        v-model="completionDialog"
      >
        <v-card class="text-center pa-10 loaders-transition">
          <v-progress-circular
            color="blue"
            size="160"
            width="15"
            indeterminate
            v-if="processFileLoading == true"
          >
            Processing
          </v-progress-circular>
          <div v-if="processFileLoading == false">


            <v-icon
              style="font-size:160px"
              class="loaders-transition"
              color="green"
            >mdi-check-circle-outline</v-icon>
            <div class="display-1">
              <v-icon x-large>mdi-arrow-down</v-icon>
              Your files are available below.
              <v-icon x-large>mdi-arrow-down</v-icon>
            </div>
            <div class="mt-5">
              <v-btn class="mx-2" @click="completionDialog = false">Make Edits</v-btn>
              <v-btn color="primary" @click="$router.push({name:'Landing'})">Close Tool</v-btn>
            </div>

          </div>



        </v-card>
      </v-dialog>

















  </v-container>

</template>
<script>
import axios from 'axios'
import FileDownload from 'js-file-download'
import DataValidation from '@/components/DataValidation'
import StepHeading from '@/components/StepHeading'
import ErrorMessage from '@/components/ErrorMessage'

export default {
  name: 'TrainTestSplit',
  components: {
    DataValidation,
    StepHeading,
    ErrorMessage
  },
  data() {
    return {
      e1: 1,

      file: null,
      fileData: null,
      fileDataValid: null,
      fileDataLoading: false,

      prevalenceOption: 0,

      //STEP 2
      targetColumn: null,
      targetColumnList: [],
      classMetadata: null,
      //class computed
      class0size: 0,
      class0percent: 0,
      class0nanSize: 0,
      class0nanPercent: 0,
      class1size: 0,
      class1percent: 0,
      class1nanSize: 0,
      class1nanPercent: 0,

      placeholderSlot: 100,

      minSampleSize:50,
      maxSampleSize:100, //changed programatically
      trainingClassSampleSize: 0,
      widthTest: 30,
      barSizes: {
        nan: 0,
        train0: 0,
        train1: 0,
        test0: 0,
        test1: 0,
        extra: 0
      },
      barData: {
        test0global: 0,
        test1global: 0,
        extra: 0
      },
      outputFiles: {
        training: null,
        testing: null,
        nan: null,
        extra:null
      },
      outputSettings: {
        includeRowIndex: false,
        nanFile: false,
        extraFile: false,
      },
      completionDialog: false,
      processFileLoading: false,
    }
  },
  computed: {
    //Control Which Steps Shows,
    showStep2() {
      if (
        this.fileData != null
        && (this.fileDataValid ? this.fileDataValid.bool : false) // if data field exists
      ) {
        return true
      } else {
        return false
      }

    },
    showStep3() {
      if (
        this.showStep2
        && this.targetColumn != null
        && !this.minSampleSizeError
      ) {
        return true
      } else {
        return false
      }

    },
    showStep4() {
      if (
        this.showStep3
      ) {
        return true
      } else {
        return false
      }

    },
    //Errors
    minSampleSizeError() {
      if (this.classMetadata != null) {
        if (this.classMetadata.class_counts[0] < this.minSampleSize || this.classMetadata.class_counts[1] < this.minSampleSize) {
          return true
        }

        else {
          return false
        }
      }
      return false
    }

  },
  methods: {
    resetStep1() {
      this.file = null
      this.fileData = null
      this.fileDataValid = null
      this.targetColumnList = []
      this.resetStep2()

    },
    resetStep2() {
      this.targetColumn = null
      this.classMetadata = null
      this.class0size = 0
      this.class0percent = 0
      this.class0nanSize = 0
      this.class0nanPercent = 0
      this.class1size = 0
      this.class1percent = 0
      this.class1nanSize = 0
      this.class1nanPercent = 0
      this.placeholderSlot = 100

      this.resetStep3()
    },
    resetStep3() {
      console.log('reset step 3')

    },

    fileUpload(file) {
      if (file != null) {
        //this method uploads form data
        var formData = new FormData();

        //UI
        this.fileDataLoading = true

        //file name data stored in X-file header of post request
        formData.append("file", file);
        axios.post('/data_file_upload', formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            'X-filename': file.name,
            'X-filegroup': 'train_test_split'

          }
        }).then(result => {
          this.fileDataLoading = false
          //file data stored in data field of result
          this.fileData = result.data

          //set target column options
          this.targetColumnList = this.fileData.column_names.reverse()

        }).catch(() => {
          this.fileDataLoading = false
          this.$store.commit('snackbarMessageSet', {
            color: 'red lighten-1',
            message: 'Error processing file.'
          })
          this.resetStep1()
        })
      }
      else {
        this.fileDataLoading = false
        this.resetStep1()
      }

    },
    fileValidationData(result){
      console.log(result)
      this.fileDataValid = result
    },


    determineClassMetadata(field){
      if (field != null) {
        let data = {
          target_column: this.targetColumn,
          storage_id: this.fileData.storage_id
        }
        return axios.post('train_test_split/metadata', data, {
          headers: {
          'Content-Type': 'application/json',
          }
        }).then(result => {
          //Parse JSON in subobjects
          this.classMetadata = result.data
          this.classMetadata.class_counts = JSON.parse(this.classMetadata.class_counts)

          //If missing data, process the counts
          if (this.classMetadata.nan_class_counts != null) {
            this.classMetadata.nan_class_counts = JSON.parse(this.classMetadata.nan_class_counts)
          }

          //Calculated values and UI parameters
          //Step 2
          this.calculateMetadataMetrics() //for Step 2 bar
          //Step 3
          this.findTrainingClassSampleSize()
          this.calculatePercentage() //for Step 3
          //Step 4
          this.makeFileNames()



        }).catch(() => {
          this.$store.commit('snackbarMessageSet', {
            color: 'red lighten-1',
            message: 'Invalid column selection. Values are not binary.'
          })
          this.resetStep2()

        })
      }
      else {
        this.resetStep2()
      }

    },
    makeFileNames() {
      let fn = this.file.name.trim()
      fn = fn.replace('.csv', '')
      fn = fn.trim()
      this.outputFiles.training = fn + '_training'
      this.outputFiles.testing = fn + '_testing'
      this.outputFiles.extra = fn + '_extra'
      this.outputFiles.nan = fn + '_missing_data'
    },
    processFiles() {
      let data = {
        target_column: this.targetColumn,
        storage_id: this.fileData.storage_id,
        training_class_sample_size: this.trainingClassSampleSize, //Not matched to output
        prevalence_option: this.prevalenceOption, //0 = use all data, 1 = maintain initail prevalence
        majority_class: this.classMetadata.majority_class,
        extra: this.barData.extra, // extra data used in maintaining inital prevalence
        include_index: this.outputSettings.includeRowIndex

      }

      //UI elements
      this.completionDialog = true
      this.processFileLoading = true

      return axios.post('train_test_split/process', data, {
        headers: {
        'Content-Type': 'application/json',
        }
      }).then(response => {
        console.log(response)

        //UI elements
        this.processFileLoading = false

        //File elements
        FileDownload(response.data.training, this.outputFiles.training + '.csv')
        FileDownload(response.data.testing, this.outputFiles.testing + '.csv')
        if (this.outputSettings.extraFile) {
          FileDownload(response.data.extra, this.outputFiles.extra + '.csv')
        }
        if (this.outputSettings.nanFile) {
          try {
            FileDownload(response.data.nan, this.outputFiles.nan + '.csv')
          }
          catch(err) {
            console.log('error')
          }

        }
      })

    },
    findTrainingClassSampleSize() {
      let minortyCount = this.classMetadata.class_counts[this.classMetadata.minority_class]
      let halfMinorityCount = Math.round(minortyCount / 2)
      this.maxSampleSize = minortyCount
      if (this.minSampleSize > halfMinorityCount) {
        this.trainingClassSampleSize = this.minSampleSize
      }
      else {
        this.trainingClassSampleSize = halfMinorityCount
      }
    },

    calculateMetadataMetrics() {
      this.class0size = this.classMetadata.class_counts[0]
      this.class1size = this.classMetadata.class_counts[1]
      this.class0percent = Math.round(1000 * (this.classMetadata.class_counts[0] / this.classMetadata.total_count)) / 10
      this.class1percent = Math.round(1000 * (this.classMetadata.class_counts[1] / this.classMetadata.total_count)) / 10
      this.placeholderSlot = 0
      if (this.classMetadata.nan_class_counts != null) {
        this.class0nanSize = this.classMetadata.nan_class_counts[0]
        this.class0nanPercent = Math.round(1000 * (this.classMetadata.nan_class_counts[0] / this.classMetadata.class_counts[0])) / 10

        this.class1nanSize = this.classMetadata.nan_class_counts[1]
        this.class1nanPercent = Math.round(1000 * (this.classMetadata.nan_class_counts[1] / this.classMetadata.class_counts[1])) / 10

      }
    },
    calculatePercentage() {
      if (this.prevalenceOption == 0) {

        if (this.classMetadata.nan_class_counts != null) {
          this.barSizes.nan = 100 * ( (this.classMetadata.nan_class_counts[0] +  this.classMetadata.nan_class_counts[1]) / this.classMetadata.total_count)

          this.barSizes.train0 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)
          this.barSizes.train1 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)

          this.barSizes.test0 = 100 * (this.classMetadata.class_counts[0] - this.trainingClassSampleSize - (this.classMetadata.nan_class_counts[0] +  this.classMetadata.nan_class_counts[1])) / this.classMetadata.total_count
          this.barSizes.test1 = 100 * (this.classMetadata.class_counts[1] - this.trainingClassSampleSize - (this.classMetadata.nan_class_counts[0] +  this.classMetadata.nan_class_counts[1])) / this.classMetadata.total_count
          this.barSizes.extra = 0

          this.barData.test0global = this.classMetadata.class_counts[0] - this.trainingClassSampleSize - this.classMetadata.nan_class_counts[0]
          this.barData.test1global = this.classMetadata.class_counts[1] - this.trainingClassSampleSize - this.classMetadata.nan_class_counts[1]
          this.barData.extra = 0

        }

        else {
          this.barSizes.train0 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)
          this.barSizes.train1 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)
          this.barSizes.test0 = 100 * (this.classMetadata.class_counts[0] - this.trainingClassSampleSize) / this.classMetadata.total_count
          this.barSizes.test1 = 100 * (this.classMetadata.class_counts[1] - this.trainingClassSampleSize) / this.classMetadata.total_count
          this.barSizes.extra = 0

          this.barData.test0global = this.classMetadata.class_counts[0] - this.trainingClassSampleSize
          this.barData.test1global = this.classMetadata.class_counts[1] - this.trainingClassSampleSize
          this.barData.extra = 0

        }

      }
      else if (this.prevalenceOption == 1) {

        if (this.classMetadata.nan_class_counts != null) {

          this.barSizes.nan = 100 * ( (this.classMetadata.nan_class_counts[0] +  this.classMetadata.nan_class_counts[1]) / this.classMetadata.total_count)

          this.barSizes.train0 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)
          this.barSizes.train1 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)

          let percentMajority = this.classMetadata.class_counts[this.classMetadata.majority_class] / this.classMetadata.total_count
          let percentMinority = this.classMetadata.class_counts[this.classMetadata.minority_class] / this.classMetadata.total_count

          let minorityRemain = this.classMetadata.class_counts[this.classMetadata.minority_class] - this.trainingClassSampleSize - this.classMetadata.nan_class_counts[this.classMetadata.minority_class]
          let totalRemain = Math.round(minorityRemain / percentMinority)
          let majorityRemain = Math.round(percentMajority * totalRemain)

          let numberToDrop = this.classMetadata.class_counts[this.classMetadata.majority_class] - this.trainingClassSampleSize - majorityRemain - this.classMetadata.nan_class_counts[this.classMetadata.majority_class]


          if (this.classMetadata.majority_class == 0) {
            this.barSizes.test0 = 100 * majorityRemain / this.classMetadata.total_count
            this.barSizes.test1 = 100 * minorityRemain / this.classMetadata.total_count
            this.barData.test0global = majorityRemain
            this.barData.test1global = minorityRemain

          }
          else if (this.classMetadata.majority_class == 1) {
            this.barSizes.test0 = 100 * minorityRemain / this.classMetadata.total_count
            this.barSizes.test1 = 100 * majorityRemain / this.classMetadata.total_count
            this.barData.test0global = minorityRemain
            this.barData.test1global = majorityRemain
          }
          this.barData.extra = numberToDrop
          this.barSizes.extra = 100 * numberToDrop / this.classMetadata.total_count



        }

        else {
          this.barSizes.train0 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)
          this.barSizes.train1 = 100 * (this.trainingClassSampleSize / this.classMetadata.total_count)


          let percentMajority = this.classMetadata.class_counts[this.classMetadata.majority_class] / this.classMetadata.total_count
          let percentMinority = this.classMetadata.class_counts[this.classMetadata.minority_class] / this.classMetadata.total_count
          let minorityRemain = this.classMetadata.class_counts[this.classMetadata.minority_class] - this.trainingClassSampleSize
          let totalRemain = Math.round(minorityRemain / percentMinority)
          let majorityRemain = Math.round(percentMajority * totalRemain)
          let numberToDrop = this.classMetadata.class_counts[this.classMetadata.majority_class] - this.trainingClassSampleSize - majorityRemain


          if (this.classMetadata.majority_class == 0) {
            this.barSizes.test0 = 100 * majorityRemain / this.classMetadata.total_count
            this.barSizes.test1 = 100 * minorityRemain / this.classMetadata.total_count
            this.barData.test0global = majorityRemain
            this.barData.test1global = minorityRemain

          }
          else if (this.classMetadata.majority_class == 1) {
            this.barSizes.test0 = 100 * minorityRemain / this.classMetadata.total_count
            this.barSizes.test1 = 100 * majorityRemain / this.classMetadata.total_count
            this.barData.test0global = minorityRemain
            this.barData.test1global = majorityRemain
          }
          this.barData.extra = numberToDrop
          this.barSizes.extra = 100 * numberToDrop / this.classMetadata.total_count

        }


      }


    },



  }

}
</script>
<style>
.distrobution-box {
  padding-top:16px;
  height: 80px;
  transition: width 0.5s;
  display: inline-block;
  text-align: center;
  color: white;
  overflow: hidden;
}
.title-box {
  padding-top:5px;
  height: 30px;
  transition: width 0.5s;
  display: inline-block;
  text-align: center;
  color: white;
  overflow: hidden;
}

.loaders-transition {
  transition: 0.5s;
}


</style>
