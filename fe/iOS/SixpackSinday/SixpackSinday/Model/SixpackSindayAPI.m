//
//  SixpackSindayAPI.m
//  SixpackSinday
//
//  Created by Dru Lang on 4/7/14.
//  Copyright (c) 2014 drulang. All rights reserved.
//

#import "SixpackSindayAPI.h"
#import "User.h"
#import "UserToken.h"

#define MESSAGE_OK  = "OK"
#define MESSAGE_ERR = "ERR"


static const NSString *SPSHOST = @"localhost";
static const NSUInteger SPSPORT = 5000;
static const NSString *APITOKEN = @"testtoken";

@interface SixpackSindayAPI()

@property (strong, nonatomic) NSString *spsBaseURL;
@property  (strong, nonatomic)NSString *spsAppTokenParam;

@end

@implementation SixpackSindayAPI

#pragma  mark  Properties

- (NSString *)spsBaseURL {
    if (!_spsBaseURL) _spsBaseURL = [NSString stringWithFormat:@"http://%@:%d", SPSHOST, SPSPORT];
    return _spsBaseURL;
}

- (NSString *)spsAppTokenParam {
    if (!_spsAppTokenParam) _spsAppTokenParam = [NSString stringWithFormat:@"apptoken=%@", APITOKEN];
    return _spsAppTokenParam;
}

#pragma mark Methods

- (BOOL) systemUp {

    NSString *urlString = [NSString stringWithFormat:@"%@/system", self.spsBaseURL];
    NSURL *url = [NSURL URLWithString:urlString];
    
    NSError *error = nil;
    NSURLResponse *response;
    
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    NSData *data = [NSURLConnection sendSynchronousRequest:request
                                                        returningResponse:&response
                                                                    error:&error];
    
    NSDictionary *jsonData = [NSJSONSerialization JSONObjectWithData: data options:0 error:&error];
    
    if ([jsonData[@"apistatus"] isEqualToString:@"UP"]){
        return YES;
    } else {
        return NO;
    }

}

- (User *) createUserWithUserName:(NSString *)username
                       setEmailTo:(NSString *)email
                    setPasswordTo:(NSString *)password {
    
    NSString *urlString = [NSString stringWithFormat:@"%@/user?%@", self.spsBaseURL, self.spsAppTokenParam];
    NSURL *url = [NSURL URLWithString:urlString];
    
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    request.HTTPMethod = @"POST";
    
    NSString *requestStr = [NSString stringWithFormat:@"email=%@&username=%@&password=%@", email, username, password];
    NSData *requestData = [NSData dataWithBytes:[requestStr UTF8String] length:[requestStr length]];
    [request setValue:@"application/x-www-form-urlencoded" forHTTPHeaderField:@"content-type"];
    [request setHTTPBody:requestData];
    
    NSURLResponse *response = nil;
    NSError *error = nil;
    
    NSData *returnData = [NSURLConnection sendSynchronousRequest:request returningResponse:&response error:&error];
    NSDictionary *jsonData = [NSJSONSerialization JSONObjectWithData:returnData options:0 error:&error];
    
    
    if ([jsonData[@"status"] isEqualToString:@"OK"]) {
        User *u = [[User alloc] init];
        u.firstName = [jsonData valueForKeyPath:@"user.firstname"];
        u.lastName = [jsonData valueForKeyPath:@"user.lastname"];
        u.email = [jsonData valueForKeyPath:@"user.email"];
        u.username = [jsonData valueForKeyPath:@"user.username"];
        u.userID = (NSUInteger)[jsonData valueForKeyPath:@"user.userid"];
        
        //Setup User Token
        UserToken *ut = [[UserToken alloc] init];
        ut.token = [jsonData valueForKeyPath:@"usertoken.token"];
        u.userToken = ut;
        return u;
        
    } else {
        //What to do?
    }

    return nil;
}

@end
