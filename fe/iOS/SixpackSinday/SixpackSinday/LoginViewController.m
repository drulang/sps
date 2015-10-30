//
//  LoginViewController.m
//  SixpackSinday
//
//  Created by Dru Lang on 4/7/14.
//  Copyright (c) 2014 drulang. All rights reserved.
//

#import "LoginViewController.h"
#import "SixpackSindayAPI.h"

@interface LoginViewController ()
@property (weak, nonatomic) IBOutlet UILabel *errorMessage;

@end

@implementation LoginViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    SixpackSindayAPI *api = [[SixpackSindayAPI alloc] init];
    if([api systemUp]) {
        self.errorMessage.hidden = YES;
    }
    else {
        self.errorMessage.text = @"Unable to connect to server. Please try again later.";
        self.errorMessage.hidden = NO;
    }
    
    [api createUserWithUserName:@"iosu" setEmailTo:@"iosemail" setPasswordTo:@"isopw"];
}


/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
