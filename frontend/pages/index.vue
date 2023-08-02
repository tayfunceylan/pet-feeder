<template>
    <v-card class="mx-auto" max-width="600">
      <v-toolbar color="secondary">
        <v-toolbar-title></v-toolbar-title>
        
        <v-spacer></v-spacer>
        <v-btn>&lt</v-btn>
        <v-btn>Heute</v-btn>
        <v-btn>></v-btn>
        <v-spacer></v-spacer>
  
        <v-btn variant="text" icon="mdi-cog"></v-btn>
      </v-toolbar>
  
      <v-list lines="one">
        <v-list-subheader>Nassfutter</v-list-subheader>
  
        <v-list-item
          v-for="folder in folders"
          :key="folder.title"
          :title="folder.title"
          :subtitle="folder.subtitle"
        >
          <template v-slot:prepend>
            <v-avatar color="grey-lighten-1">
              <v-icon color="white">mdi-folder</v-icon>
            </v-avatar>
            <v-avatar color="grey-lighten-1">
              <v-icon color="white">mdi-folder</v-icon>
            </v-avatar>
          </template>
  
          <template v-slot:append>
            <v-btn
              color="grey-lighten-1"
              icon="mdi-information"
              variant="text"
            ></v-btn>
          </template>
        </v-list-item>
  
        <v-divider inset></v-divider>
        
      </v-list>
    </v-card>
  </template>
  <script>
    export default {
      data: () => ({
        folders: [
          {
            title: '60g',
            subtitle: '8:00 Uhr',
          },
          {
            title: '80',
            subtitle: '14:00 Uhr',
          },
          {
            title: '100g',
            subtitle: '18:00 Uhr',
          },
        ],
      }),
    }
  </script>