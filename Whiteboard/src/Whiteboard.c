//
//  Whiteboard
//
//  Created by Ingenuity i/o on 2024/10/18.
//  Copyright © 2023 Ingenuity i/o. All rights reserved.
//

#include "Whiteboard.h"
#include <string.h>

struct _Whiteboard_t {
    //inputs
    // "title"
    char * TitleI;
    // "backgroundColor"
    char * BackgroundcolorI;
    // "labelsVisible"
    bool LabelsvisibleI;
    // "chatMessage"
    char * ChatmessageI;
    // "ui_command"
    char * Ui_CommandI;

    //outputs
    // "lastChatMessage"
    char * LastchatmessageO;
    // "lastAction"
    char * LastactionO;
    // "ui_error"
    char * Ui_ErrorO;
};


Whiteboard_t *Whiteboard_new (void){
    Whiteboard_t *agent = (Whiteboard_t *) calloc(1, sizeof(Whiteboard_t));

    //add code here if needed

    return agent;
}

void Whiteboard_destroy (Whiteboard_t **agent){
    if (agent != NULL && *agent != NULL){
        if ((*agent)->TitleI != NULL){
            free((*agent)->TitleI);
            (*agent)->TitleI = NULL;
        }
        if ((*agent)->BackgroundcolorI != NULL){
            free((*agent)->BackgroundcolorI);
            (*agent)->BackgroundcolorI = NULL;
        }
        if ((*agent)->ChatmessageI != NULL){
            free((*agent)->ChatmessageI);
            (*agent)->ChatmessageI = NULL;
        }
        if ((*agent)->Ui_CommandI != NULL){
            free((*agent)->Ui_CommandI);
            (*agent)->Ui_CommandI = NULL;
        }
        if ((*agent)->LastchatmessageO != NULL){
            free((*agent)->LastchatmessageO);
            (*agent)->LastchatmessageO = NULL;
        }
        if ((*agent)->LastactionO != NULL){
            free((*agent)->LastactionO);
            (*agent)->LastactionO = NULL;
        }
        if ((*agent)->Ui_ErrorO != NULL){
            free((*agent)->Ui_ErrorO);
            (*agent)->Ui_ErrorO = NULL;
        }
        free(*agent);
        *agent = NULL;
    }
}

/////////////////////////////////////////////////////////////////////
//inputs
// title
void Whiteboard_setTitleI(Whiteboard_t *agent, char * value){
    assert(agent);
    if (agent->TitleI != NULL)
        free(agent->TitleI);
    char *text = (char *)calloc(1, strlen((char *)value) + 1);
    agent->TitleI = (value == NULL)? NULL : memcpy(text, value, strlen((char *)value) + 1);

    //add code here if needed

}
char * Whiteboard_getTitleI(Whiteboard_t *agent){
    assert(agent);
    //FIXME: decide if we do a copy here or not
    return agent->TitleI;
}

// backgroundColor
void Whiteboard_setBackgroundcolorI(Whiteboard_t *agent, char * value){
    assert(agent);
    if (agent->BackgroundcolorI != NULL)
        free(agent->BackgroundcolorI);
    char *text = (char *)calloc(1, strlen((char *)value) + 1);
    agent->BackgroundcolorI = (value == NULL)? NULL : memcpy(text, value, strlen((char *)value) + 1);

    //add code here if needed

}
char * Whiteboard_getBackgroundcolorI(Whiteboard_t *agent){
    assert(agent);
    //FIXME: decide if we do a copy here or not
    return agent->BackgroundcolorI;
}

// labelsVisible
void Whiteboard_setLabelsvisibleI(Whiteboard_t *agent, bool value){
    assert(agent);
    agent->LabelsvisibleI = value;

    //add code here if needed

}
bool Whiteboard_getLabelsvisibleI(Whiteboard_t *agent){
    assert(agent);
    return agent->LabelsvisibleI;
}

// chatMessage
void Whiteboard_setChatmessageI(Whiteboard_t *agent, char * value){
    assert(agent);
    if (agent->ChatmessageI != NULL)
        free(agent->ChatmessageI);
    char *text = (char *)calloc(1, strlen((char *)value) + 1);
    agent->ChatmessageI = (value == NULL)? NULL : memcpy(text, value, strlen((char *)value) + 1);

    //add code here if needed

}
char * Whiteboard_getChatmessageI(Whiteboard_t *agent){
    assert(agent);
    //FIXME: decide if we do a copy here or not
    return agent->ChatmessageI;
}

// clear
void Whiteboard_setClearI(Whiteboard_t *agent){
    assert(agent);

    //add code here if needed

}

// ui_command
void Whiteboard_setUi_CommandI(Whiteboard_t *agent, char * value){
    assert(agent);
    if (agent->Ui_CommandI != NULL)
        free(agent->Ui_CommandI);
    char *text = (char *)calloc(1, strlen((char *)value) + 1);
    agent->Ui_CommandI = (value == NULL)? NULL : memcpy(text, value, strlen((char *)value) + 1);

    //add code here if needed

}
char * Whiteboard_getUi_CommandI(Whiteboard_t *agent){
    assert(agent);
    //FIXME: decide if we do a copy here or not
    return agent->Ui_CommandI;
}

/////////////////////////////////////////////////////////////////////
//outputs
// lastChatMessage
void Whiteboard_setLastchatmessageO(Whiteboard_t *agent, char * value){
    assert(agent);
    if (agent->LastchatmessageO != NULL)
        free(agent->LastchatmessageO);
    char *text = (char *)calloc(1, strlen((char *)value) + 1);
    agent->LastchatmessageO = (value == NULL)? NULL : memcpy(text, value, strlen((char *)value) + 1);

    //add code here if needed

    igs_output_set_string("lastChatMessage", agent->LastchatmessageO);
}
char * Whiteboard_getLastchatmessageO(Whiteboard_t *agent){
    assert(agent);
    //FIXME: decide if we do a copy here or not
    return agent->LastchatmessageO;
}

// lastAction
void Whiteboard_setLastactionO(Whiteboard_t *agent, char * value){
    assert(agent);
    if (agent->LastactionO != NULL)
        free(agent->LastactionO);
    char *text = (char *)calloc(1, strlen((char *)value) + 1);
    agent->LastactionO = (value == NULL)? NULL : memcpy(text, value, strlen((char *)value) + 1);

    //add code here if needed

    igs_output_set_string("lastAction", agent->LastactionO);
}
char * Whiteboard_getLastactionO(Whiteboard_t *agent){
    assert(agent);
    //FIXME: decide if we do a copy here or not
    return agent->LastactionO;
}

// ui_error
void Whiteboard_setUi_ErrorO(Whiteboard_t *agent, char * value){
    assert(agent);
    if (agent->Ui_ErrorO != NULL)
        free(agent->Ui_ErrorO);
    char *text = (char *)calloc(1, strlen((char *)value) + 1);
    agent->Ui_ErrorO = (value == NULL)? NULL : memcpy(text, value, strlen((char *)value) + 1);

    //add code here if needed

    igs_output_set_string("ui_error", agent->Ui_ErrorO);
}
char * Whiteboard_getUi_ErrorO(Whiteboard_t *agent){
    assert(agent);
    //FIXME: decide if we do a copy here or not
    return agent->Ui_ErrorO;
}

/////////////////////////////////////////////////////////////////////
//services
void Whiteboard_Chat(Whiteboard_t *agent, char * Message){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Snapshot(Whiteboard_t *agent){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Clear(Whiteboard_t *agent){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Showlabels(Whiteboard_t *agent){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Hidelabels(Whiteboard_t *agent){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Addshape(Whiteboard_t *agent, char * Type, double X, double Y, double Width, double Height, char * Fill, char * Stroke, double Strokewidth){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Addtext(Whiteboard_t *agent, char * Text, double X, double Y, char * Color){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Addimage(Whiteboard_t *agent, void * Base64, size_t Base64_size, double X, double Y, double Width, double Height){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Addimagefromurl(Whiteboard_t *agent, char * Url, double X, double Y){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Remove(Whiteboard_t *agent, int Elementid){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Translate(Whiteboard_t *agent, int Elementid, double Dx, double Dy){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Moveto(Whiteboard_t *agent, int Elementid, double X, double Y){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Setstringproperty(Whiteboard_t *agent, int Elementid, char * Property, char * Value){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Setdoubleproperty(Whiteboard_t *agent, int Elementid, char * Property, double Value){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Getelementids(Whiteboard_t *agent){
    assert(agent);

    //add code here if needed

}

void Whiteboard_Getelements(Whiteboard_t *agent){
    assert(agent);

    //add code here if needed

}

