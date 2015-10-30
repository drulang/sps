//
//  User.h
//  SixpackSinday
//
//  Created by Dru Lang on 4/7/14.
//  Copyright (c) 2014 drulang. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "UserToken.h"

@interface User : NSObject

@property (nonatomic) NSUInteger userID;
@property (nonatomic, strong) NSString *username;
@property (nonatomic, strong) NSString *email;
@property (nonatomic, strong) NSString *firstName;
@property (nonatomic, strong) NSString *lastName;
@property (nonatomic, strong) UserToken *userToken;

@end
