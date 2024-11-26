//
//  Whiteboard
//  Created by Ingenuity i/o on 2024/10/18
//
//  no description
//  Copyright © 2023 Ingenuity i/o. All rights reserved.
//
#ifndef Whiteboard_h
#define Whiteboard_h

#include <ingescape/ingescape.h>

typedef struct _Whiteboard_t Whiteboard_t;
Whiteboard_t* Whiteboard_new (void);
void Whiteboard_destroy (Whiteboard_t **agent);

//inputs
// "title"
void Whiteboard_setTitleI(Whiteboard_t *agent, char * value);
char * Whiteboard_getTitleI(Whiteboard_t *agent);
// "backgroundColor"
void Whiteboard_setBackgroundcolorI(Whiteboard_t *agent, char * value);
char * Whiteboard_getBackgroundcolorI(Whiteboard_t *agent);
// "labelsVisible"
void Whiteboard_setLabelsvisibleI(Whiteboard_t *agent, bool value);
bool Whiteboard_getLabelsvisibleI(Whiteboard_t *agent);
// "chatMessage"
void Whiteboard_setChatmessageI(Whiteboard_t *agent, char * value);
char * Whiteboard_getChatmessageI(Whiteboard_t *agent);
// "clear"
void Whiteboard_setClearI(Whiteboard_t *agent);
// "ui_command"
void Whiteboard_setUi_CommandI(Whiteboard_t *agent, char * value);
char * Whiteboard_getUi_CommandI(Whiteboard_t *agent);

//outputs
// "lastChatMessage"
void Whiteboard_setLastchatmessageO(Whiteboard_t *agent, char * value);
char * Whiteboard_getLastchatmessageO(Whiteboard_t *agent);
// "lastAction"
void Whiteboard_setLastactionO(Whiteboard_t *agent, char * value);
char * Whiteboard_getLastactionO(Whiteboard_t *agent);
// "ui_error"
void Whiteboard_setUi_ErrorO(Whiteboard_t *agent, char * value);
char * Whiteboard_getUi_ErrorO(Whiteboard_t *agent);

//services
// "chat"
void Whiteboard_Chat(Whiteboard_t *agent, char * Message);
// "snapshot"
void Whiteboard_Snapshot(Whiteboard_t *agent);
);
// "clear"
void Whiteboard_Clear(Whiteboard_t *agent);
);
// "showLabels"
void Whiteboard_Showlabels(Whiteboard_t *agent);
);
// "hideLabels"
void Whiteboard_Hidelabels(Whiteboard_t *agent);
);
// "addShape"
void Whiteboard_Addshape(Whiteboard_t *agent, char * Type, double X, double Y, double Width, double Height, char * Fill, char * Stroke, double Strokewidth);
// "addText"
void Whiteboard_Addtext(Whiteboard_t *agent, char * Text, double X, double Y, char * Color);
// "addImage"
void Whiteboard_Addimage(Whiteboard_t *agent, void * Base64, size_t Base64_size, double X, double Y, double Width, double Height);
// "addImageFromUrl"
void Whiteboard_Addimagefromurl(Whiteboard_t *agent, char * Url, double X, double Y);
// "remove"
void Whiteboard_Remove(Whiteboard_t *agent, int Elementid);
// "translate"
void Whiteboard_Translate(Whiteboard_t *agent, int Elementid, double Dx, double Dy);
// "moveTo"
void Whiteboard_Moveto(Whiteboard_t *agent, int Elementid, double X, double Y);
// "setStringProperty"
void Whiteboard_Setstringproperty(Whiteboard_t *agent, int Elementid, char * Property, char * Value);
// "setDoubleProperty"
void Whiteboard_Setdoubleproperty(Whiteboard_t *agent, int Elementid, char * Property, double Value);
// "getElementIds"
void Whiteboard_Getelementids(Whiteboard_t *agent);
);
// "getElements"
void Whiteboard_Getelements(Whiteboard_t *agent);
);

#endif /* Whiteboard_h */
