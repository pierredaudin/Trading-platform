//
//  main.c
//  Whiteboard
//  Created by Ingenuity i/o on 2024/10/18
//
//  no description
//  Copyright © 2023 Ingenuity i/o. All rights reserved.
//

#if defined(__unix__) || defined(__linux__) || (defined(__APPLE__) && defined(__MACH__))
    #include <pthread.h>
#elif (defined WIN32 || defined _WIN32)
    #ifndef WIN32_LEAN_AND_MEAN
        #define WIN32_LEAN_AND_MEAN
    #endif
    #define NOMINMAX
    #include <windows.h>
    #include <winsock2.h>
#endif

#include <ingescape/ingescape.h>
#include <getopt.h>
#include "Whiteboard.h"

//default agent parameters to be overriden by command line parameters
#define PORT 5670
#define AGENT_NAME "Whiteboard"
#define DEVICE NULL
#define IS_VERBOSE false
#define STRING_SIZE 4096

int ingescapeSentMessage(zloop_t *loop, zsock_t *reader, void *arg){
    char *message = NULL;
    zsock_recv(reader, "s", &message);
    if (streq(message, "LOOP_STOPPED")){
        igs_info("LOOP_STOPPED received from Ingescape");
        return -1;
    }else
        return 0;
}

//inputs
// "title" callback
void TitleInputCallback(igs_io_type_t ioType, const char* name, igs_io_value_type_t valueType,
                        void* value, size_t valueSize, void* myData) {
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    char *v = (char *)value;
    igs_info("%s changed to %s", name, v);
    Whiteboard_setTitleI(agent, v);
}

// "backgroundColor" callback
void BackgroundcolorInputCallback(igs_io_type_t ioType, const char* name, igs_io_value_type_t valueType,
                        void* value, size_t valueSize, void* myData) {
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    char *v = (char *)value;
    igs_info("%s changed to %s", name, v);
    Whiteboard_setBackgroundcolorI(agent, v);
}

// "labelsVisible" callback
void LabelsvisibleInputCallback(igs_io_type_t ioType, const char* name, igs_io_value_type_t valueType,
                        void* value, size_t valueSize, void* myData) {
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    bool v = *(bool *)value;
    igs_info("%s changed to %d", name, v);
    Whiteboard_setLabelsvisibleI(agent, v);
}

// "chatMessage" callback
void ChatmessageInputCallback(igs_io_type_t ioType, const char* name, igs_io_value_type_t valueType,
                        void* value, size_t valueSize, void* myData) {
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    char *v = (char *)value;
    igs_info("%s changed to %s", name, v);
    Whiteboard_setChatmessageI(agent, v);
}

// "clear" callback
void ClearInputCallback(igs_io_type_t ioType, const char* name, igs_io_value_type_t valueType,
                        void* value, size_t valueSize, void* myData) {
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    igs_info("%s changed (impulsion)", name);
    Whiteboard_setClearI(agent);
}

// "ui_command" callback
void Ui_CommandInputCallback(igs_io_type_t ioType, const char* name, igs_io_value_type_t valueType,
                        void* value, size_t valueSize, void* myData) {
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    char *v = (char *)value;
    igs_info("%s changed to %s", name, v);
    Whiteboard_setUi_CommandI(agent, v);
}

//attributes
//services
// "chat" callback
void ChatCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    char * Message = firstArgument->c;

    Whiteboard_Chat(agent, Message);
}
// "snapshot" callback
void SnapshotCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;

    Whiteboard_Snapshot(agent);
}
// "clear" callback
void ClearCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;

    Whiteboard_Clear(agent);
}
// "showLabels" callback
void ShowlabelsCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;

    Whiteboard_Showlabels(agent);
}
// "hideLabels" callback
void HidelabelsCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;

    Whiteboard_Hidelabels(agent);
}
// "addShape" callback
void AddshapeCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    char * Type = firstArgument->c;
    double X = firstArgument->next->d;
    double Y = firstArgument->next->next->d;
    double Width = firstArgument->next->next->next->d;
    double Height = firstArgument->next->next->next->next->d;
    char * Fill = firstArgument->next->next->next->next->next->c;
    char * Stroke = firstArgument->next->next->next->next->next->next->c;
    double Strokewidth = firstArgument->next->next->next->next->next->next->next->d;

    Whiteboard_Addshape(agent, Type, X, Y, Width, Height, Fill, Stroke, Strokewidth);
}
// "addText" callback
void AddtextCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    char * Text = firstArgument->c;
    double X = firstArgument->next->d;
    double Y = firstArgument->next->next->d;
    char * Color = firstArgument->next->next->next->c;

    Whiteboard_Addtext(agent, Text, X, Y, Color);
}
// "addImage" callback
void AddimageCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    void * Base64 = firstArgument->data;
    size_t Base64_size = firstArgument->size;
    double X = firstArgument->next->d;
    double Y = firstArgument->next->next->d;
    double Width = firstArgument->next->next->next->d;
    double Height = firstArgument->next->next->next->next->d;

    Whiteboard_Addimage(agent, Base64, Base64_size, X, Y, Width, Height);
}
// "addImageFromUrl" callback
void AddimagefromurlCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    char * Url = firstArgument->c;
    double X = firstArgument->next->d;
    double Y = firstArgument->next->next->d;

    Whiteboard_Addimagefromurl(agent, Url, X, Y);
}
// "remove" callback
void RemoveCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    int Elementid = firstArgument->i;

    Whiteboard_Remove(agent, Elementid);
}
// "translate" callback
void TranslateCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    int Elementid = firstArgument->i;
    double Dx = firstArgument->next->d;
    double Dy = firstArgument->next->next->d;

    Whiteboard_Translate(agent, Elementid, Dx, Dy);
}
// "moveTo" callback
void MovetoCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    int Elementid = firstArgument->i;
    double X = firstArgument->next->d;
    double Y = firstArgument->next->next->d;

    Whiteboard_Moveto(agent, Elementid, X, Y);
}
// "setStringProperty" callback
void SetstringpropertyCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    int Elementid = firstArgument->i;
    char * Property = firstArgument->next->c;
    char * Value = firstArgument->next->next->c;

    Whiteboard_Setstringproperty(agent, Elementid, Property, Value);
}
// "setDoubleProperty" callback
void SetdoublepropertyCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;
    int Elementid = firstArgument->i;
    char * Property = firstArgument->next->c;
    double Value = firstArgument->next->next->d;

    Whiteboard_Setdoubleproperty(agent, Elementid, Property, Value);
}
// "getElementIds" callback
void GetelementidsCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;

    Whiteboard_Getelementids(agent);
}
// "getElements" callback
void GetelementsCallback(const char *callerAgentName, const char *callerAgentUUID,
                          const char *serviceName, igs_service_arg_t *firstArgument, size_t nbArgs,
                          const char *token, void* myData){
    Whiteboard_t *agent = (Whiteboard_t *)myData;

    Whiteboard_Getelements(agent);
}

///////////////////////////////////////////////////////////////////////////////
// COMMAND LINE AND INTERPRETER OPTIONS
//
void print_usage(void){
    printf("Usage examples:\n");
    printf("    ./Whiteboard --verbose --device en0 --port 5670\n");
    printf("\nIngescape parameters:\n");
    printf("--verbose : enable verbose mode in the application (default is disabled)\n");
    printf("--device device_name : name of the network device to be used (useful if several devices are available)\n");
    printf("--port port_number : port used for autodiscovery between agents (default: %d)\n", PORT);
    printf("--name agent_name : published name of this agent (default: %s)\n", AGENT_NAME);
    printf("--interactiveloop : enables interactive loop to pass commands in CLI (default: false)\n");
    printf("Security:\n");
    printf("--igsCert filePath : path to a private certificate used to connect to a secure platform\n");
    printf("--publicCerts directoryPath : path to a directory providing public certificates usable by ingescape\n");
    printf("\n");
}

//resolve paths starting with ~ to absolute paths
void resolveUserPathIn(char path[], size_t maxSize) {
    if (path && strlen(path) && path[0] == '~') {
        char *temp = strdup(path+1);
#ifdef _WIN32
        char *home = getenv("USERPROFILE");
#else
        char *home = getenv("HOME");
#endif
        if (!home)
            igs_error("could not find path for home directory");
        else{
            strncpy(path, home, maxSize);
            strncat(path, temp, maxSize);
        }
        free(temp);
    }
}

void print_cli_usage(void) {
    printf("Available commands in the terminal:\n");
    printf("\t/quit : quits the agent\n");
    printf("\t/help : displays this message\n");
}

///////////////////////////////////////////////////////////////////////////////
// MAIN & OPTIONS & COMMAND INTERPRETER
//
//
int main(int argc, const char * argv[]) {
    int opt = 0;
    bool verbose = IS_VERBOSE;
    char *networkDevice = DEVICE;
    unsigned int port = PORT;
    char *agentName = AGENT_NAME;
    bool interactiveloop = false;
    char igsCertPath[IGS_MAX_PATH_LENGTH] = "";
    char publicCertsDir[IGS_MAX_PATH_LENGTH] = "";

    static struct option long_options[] = {
        {"verbose",     no_argument, 0,  'v' },
        {"device",      required_argument, 0,  'd' },
        {"port",        required_argument, 0,  'p' },
        {"name",        required_argument, 0,  'n' },
        {"interactiveloop", no_argument, 0,  'i' },
        {"help",        no_argument, 0,  'h' },
        {"igsCert",        required_argument, 0,  'c' },
        {"publicCerts",        required_argument, 0,  's' },
        {0, 0, 0, 0}
    };

    int long_index = 0;
    while ((opt = getopt_long(argc, (char *const *)argv, "", long_options, &long_index)) != -1) {
        switch (opt) {
            case 'v':
                verbose = true;
                break;
            case 'd':
                networkDevice = optarg;
                break;
            case 'p':
                port = (unsigned int)atoi(optarg);
                break;
            case 'n':
                agentName = optarg;
                break;
            case 'i':
                interactiveloop = true;
                break;
            case 'h':
                print_usage();
                exit(IGS_SUCCESS);
            case 'c':
                strncpy(igsCertPath, optarg, IGS_MAX_PATH_LENGTH);
                break;
            case 's':
                strncpy(publicCertsDir, optarg, IGS_MAX_PATH_LENGTH);
                break;
            default:
                print_usage();
                exit(IGS_FAILURE);
        }
    }

    igs_agent_set_name(agentName);
    igs_log_set_console(verbose);
    igs_log_set_file(true, NULL);
    igs_log_set_stream(verbose);
    igs_definition_set_version("");
    igs_set_command_line_from_args(argc, argv);

    igs_debug("Ingescape version: %d (protocol v%d)", igs_version(), igs_protocol());

    //security
    resolveUserPathIn(igsCertPath, IGS_MAX_PATH_LENGTH);
    if (strlen(igsCertPath) && zfile_exists(igsCertPath))
        assert(igs_enable_security(igsCertPath, publicCertsDir) == IGS_SUCCESS);
    else if (strlen(igsCertPath)){
        igs_error("Could not find Ingescape certificate file '%s': exiting", igsCertPath);
        exit(IGS_FAILURE);
    }

    if (networkDevice == NULL){
        //we have no device to start with: try to find one
        int nbD = 0;
        int nbA = 0;
        char **devices = igs_net_devices_list(&nbD);
        char **addresses = igs_net_addresses_list(&nbA);
        assert(nbD == nbA);
        if (nbD == 1){
            //we have exactly one compliant network device available: we use it
            networkDevice = strdup(devices[0]);
            igs_info("using %s as default network device (this is the only one available)", networkDevice);
        }else if (nbD == 2 && (strcmp(addresses[0], "127.0.0.1") == 0 || strcmp(addresses[1], "127.0.0.1") == 0)){
            //we have two devices, one of which is the loopback
            //pick the device that is NOT the loopback
            if (strcmp(addresses[0], "127.0.0.1") == 0){
                networkDevice = strdup(devices[1]);
            }else{
                networkDevice = strdup(devices[0]);
            }
            igs_info("using %s as default network device (this is the only one available that is not the loopback)", networkDevice);
        }else{
            if (nbD == 0){
                igs_error("No network device found: aborting.");
            }else{
                igs_error("No network device passed as command line parameter and several are available.");
                printf("Please use one of these network devices:\n");
                for (int i = 0; i < nbD; i++){
                    printf("\t%s\n", devices[i]);
                }
                printf("\n");
                print_usage();
            }
            exit(1);
        }
        igs_free_net_devices_list(devices, nbD);
        igs_free_net_addresses_list(addresses, nbD);
    }

    igs_input_create("title", IGS_STRING_T, 0, 0);
    igs_input_create("backgroundColor", IGS_STRING_T, 0, 0);
    igs_input_create("labelsVisible", IGS_BOOL_T, 0, 0);
    igs_input_create("chatMessage", IGS_STRING_T, 0, 0);
    igs_input_create("clear", IGS_IMPULSION_T, 0, 0);
    igs_input_create("ui_command", IGS_STRING_T, 0, 0);
    igs_output_create("lastChatMessage", IGS_STRING_T, 0, 0);
    igs_output_create("lastAction", IGS_STRING_T, 0, 0);
    igs_output_create("ui_error", IGS_STRING_T, 0, 0);


    //initialize agent
    Whiteboard_t *agent = Whiteboard_new ();
    igs_observe_input("title", TitleInputCallback, agent);
    igs_observe_input("backgroundColor", BackgroundcolorInputCallback, agent);
    igs_observe_input("labelsVisible", LabelsvisibleInputCallback, agent);
    igs_observe_input("chatMessage", ChatmessageInputCallback, agent);
    igs_observe_input("clear", ClearInputCallback, agent);
    igs_observe_input("ui_command", Ui_CommandInputCallback, agent);
    igs_service_init("chat", ChatCallback, agent);
    igs_service_arg_add("chat", "message", IGS_STRING_T);
    igs_service_init("snapshot", SnapshotCallback, agent);
    igs_service_reply_add("snapshot", "snapshotResult");
    igs_service_reply_arg_add("snapshot", "snapshotResult", "base64Png", IGS_DATA_T);
    igs_service_init("clear", ClearCallback, agent);
    igs_service_init("showLabels", ShowlabelsCallback, agent);
    igs_service_init("hideLabels", HidelabelsCallback, agent);
    igs_service_init("addShape", AddshapeCallback, agent);
    igs_service_arg_add("addShape", "type", IGS_STRING_T);
    igs_service_arg_add("addShape", "x", IGS_DOUBLE_T);
    igs_service_arg_add("addShape", "y", IGS_DOUBLE_T);
    igs_service_arg_add("addShape", "width", IGS_DOUBLE_T);
    igs_service_arg_add("addShape", "height", IGS_DOUBLE_T);
    igs_service_arg_add("addShape", "fill", IGS_STRING_T);
    igs_service_arg_add("addShape", "stroke", IGS_STRING_T);
    igs_service_arg_add("addShape", "strokeWidth", IGS_DOUBLE_T);
    igs_service_reply_add("addShape", "elementCreated");
    igs_service_reply_arg_add("addShape", "elementCreated", "elementId", IGS_INTEGER_T);
    igs_service_init("addText", AddtextCallback, agent);
    igs_service_arg_add("addText", "text", IGS_STRING_T);
    igs_service_arg_add("addText", "x", IGS_DOUBLE_T);
    igs_service_arg_add("addText", "y", IGS_DOUBLE_T);
    igs_service_arg_add("addText", "color", IGS_STRING_T);
    igs_service_reply_add("addText", "elementCreated");
    igs_service_reply_arg_add("addText", "elementCreated", "elementId", IGS_INTEGER_T);
    igs_service_init("addImage", AddimageCallback, agent);
    igs_service_arg_add("addImage", "base64", IGS_DATA_T);
    igs_service_arg_add("addImage", "x", IGS_DOUBLE_T);
    igs_service_arg_add("addImage", "y", IGS_DOUBLE_T);
    igs_service_arg_add("addImage", "width", IGS_DOUBLE_T);
    igs_service_arg_add("addImage", "height", IGS_DOUBLE_T);
    igs_service_reply_add("addImage", "elementCreated");
    igs_service_reply_arg_add("addImage", "elementCreated", "elementId", IGS_INTEGER_T);
    igs_service_init("addImageFromUrl", AddimagefromurlCallback, agent);
    igs_service_arg_add("addImageFromUrl", "url", IGS_STRING_T);
    igs_service_arg_add("addImageFromUrl", "x", IGS_DOUBLE_T);
    igs_service_arg_add("addImageFromUrl", "y", IGS_DOUBLE_T);
    igs_service_reply_add("addImageFromUrl", "elementCreated");
    igs_service_reply_arg_add("addImageFromUrl", "elementCreated", "elementId", IGS_INTEGER_T);
    igs_service_init("remove", RemoveCallback, agent);
    igs_service_arg_add("remove", "elementId", IGS_INTEGER_T);
    igs_service_reply_add("remove", "actionResult");
    igs_service_reply_arg_add("remove", "actionResult", "succeeded", IGS_BOOL_T);
    igs_service_init("translate", TranslateCallback, agent);
    igs_service_arg_add("translate", "elementId", IGS_INTEGER_T);
    igs_service_arg_add("translate", "dx", IGS_DOUBLE_T);
    igs_service_arg_add("translate", "dy", IGS_DOUBLE_T);
    igs_service_reply_add("translate", "actionResult");
    igs_service_reply_arg_add("translate", "actionResult", "succeeded", IGS_BOOL_T);
    igs_service_init("moveTo", MovetoCallback, agent);
    igs_service_arg_add("moveTo", "elementId", IGS_INTEGER_T);
    igs_service_arg_add("moveTo", "x", IGS_DOUBLE_T);
    igs_service_arg_add("moveTo", "y", IGS_DOUBLE_T);
    igs_service_reply_add("moveTo", "actionResult");
    igs_service_reply_arg_add("moveTo", "actionResult", "succeeded", IGS_BOOL_T);
    igs_service_init("setStringProperty", SetstringpropertyCallback, agent);
    igs_service_arg_add("setStringProperty", "elementId", IGS_INTEGER_T);
    igs_service_arg_add("setStringProperty", "property", IGS_STRING_T);
    igs_service_arg_add("setStringProperty", "value", IGS_STRING_T);
    igs_service_reply_add("setStringProperty", "actionResult");
    igs_service_reply_arg_add("setStringProperty", "actionResult", "succeeded", IGS_BOOL_T);
    igs_service_init("setDoubleProperty", SetdoublepropertyCallback, agent);
    igs_service_arg_add("setDoubleProperty", "elementId", IGS_INTEGER_T);
    igs_service_arg_add("setDoubleProperty", "property", IGS_STRING_T);
    igs_service_arg_add("setDoubleProperty", "value", IGS_DOUBLE_T);
    igs_service_reply_add("setDoubleProperty", "actionResult");
    igs_service_reply_arg_add("setDoubleProperty", "actionResult", "succeeded", IGS_BOOL_T);
    igs_service_init("getElementIds", GetelementidsCallback, agent);
    igs_service_reply_add("getElementIds", "elementIds");
    igs_service_reply_arg_add("getElementIds", "elementIds", "jsonArray", IGS_STRING_T);
    igs_service_init("getElements", GetelementsCallback, agent);
    igs_service_reply_add("getElements", "elements");
    igs_service_reply_arg_add("getElements", "elements", "jsonArray", IGS_STRING_T);

    //actually start ingescape
    igs_start_with_device(networkDevice, port);

    //mainloop management (two modes)
    if (!interactiveloop) {
        //Run the main loop (non-interactive mode):
        //we rely on CZMQ which is an ingescape dependency
        //and is thus always available.
        zloop_t *loop = zloop_new();
        zsock_t *pipe = igs_pipe_to_ingescape();
        if (pipe)
            zloop_reader(loop, pipe, ingescapeSentMessage, NULL);
        zloop_start(loop);
        zloop_destroy(&loop);
    }else{
        char message[IGS_MAX_LOG_LENGTH];
        char command[IGS_MAX_LOG_LENGTH];
        char param1[IGS_MAX_LOG_LENGTH];
        char param2[IGS_MAX_LOG_LENGTH];
        int usedChar = 0;
        print_cli_usage();
        while (igs_is_started()) {
            if (!fgets(message, IGS_MAX_LOG_LENGTH, stdin))
                break;
            if ((message[0] == '/') && (strlen(message) > 2)) {
                int matches = sscanf(message + 1, "%s %s%n%s", command, param1, &usedChar, param2);
                if (matches > 2) {
                    // copy the remaining of the message in param 2
                    strncpy(param2, message + usedChar + 2, IGS_MAX_LOG_LENGTH);
                    // remove '\n' at the end
                    param2[strnlen(param2, IGS_MAX_LOG_LENGTH) - 1] = '\0';
                }
                // Process command
                if (matches == -1) {
                    //printf("Error: could not interpret message %s\n", message + 1);
                }else if (matches == 1) {
                    if (strncmp(command, "quit", IGS_MAX_LOG_LENGTH) == 0){
                        break;
                    }else if(strncmp(command, "help", IGS_MAX_LOG_LENGTH) == 0){
                        print_cli_usage();
                    }else {
                        printf("Received command: %s\n", command);
                    }
                }else if (matches == 2) {
                    printf("Received command: %s + %s\n", command, param1);
                }else if (matches == 3) {
                    printf("Received command: %s + %s + %s\n", command, param1, param2);
                }else{
                    printf("Error: message returned %d matches (%s)\n", matches, message);
                }
            }
        }
    }

    Whiteboard_destroy (&agent);
    igs_stop();

    return 0;
}
