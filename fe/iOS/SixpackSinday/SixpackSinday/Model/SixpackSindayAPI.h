//
//  SixpackSindayAPI.h
//  SixpackSinday
//
//  Created by Dru Lang on 4/7/14.
//  Copyright (c) 2014 drulang. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "User.h"
#import "UserToken.h"

@interface SixpackSindayAPI : NSObject

- (BOOL)systemUp;

- (User *)createUserWithUserName: (NSString *)username
                      setEmailTo:(NSString *)email
                   setPasswordTo:(NSString *)password;

- (UserToken *)loginWithUsername: (NSString *)username andPassword:(NSString *)password;



@end
