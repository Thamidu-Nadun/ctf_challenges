/* =====================================================================


 *     activation code : USFE-INV-07   (XOR-encoded — "the custom value")
 *     service path    : /api/v3/register
 *     client id       : guardian_update
 *     ref             : RAVEN-17
 *
 *  Build: build.sh 
 */

#include <stdio.h>
#include <string.h>

/* --- XOR-encoded activation code. key = 0x5A. decoded at runtime. --- */
static const unsigned char K = 0x5A;
static const unsigned char ENC_CODE[] = {
    0x0F, 0x09, 0x1C, 0x1F, 0x77, 0x13, 0x14, 0x0C, 0x77, 0x6A, 0x6D
}; /* 11 bytes */


static void decode(const unsigned char *in, int n, char *out) {
    int i;
    for (i = 0; i < n; i++) {
        out[i] = (char)(in[i] ^ K);
    }
    out[n] = '\0';
}

int main(void) {
    char code[32];
    char input[64];

    decode(ENC_CODE, (int)sizeof(ENC_CODE), code);

    printf("GuardianOS Update Client v4.1.2\n");
    printf("Enter activation code: ");
    fflush(stdout);

    if (!fgets(input, sizeof(input), stdin)) {
        return 1;
    }
    input[strcspn(input, "\r\n")] = '\0';

    if (strcmp(input, code) == 0) {
        printf("Activation successful.\n");
        printf("service path : /api/v3/register\n");
        printf("client id    : guardian_update\n");
        printf("ref          : RAVEN-17\n");
        return 0;
    }

    printf("Activation failed.\n");
    return 1;
}
