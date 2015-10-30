//
//  NewProfileViewController.m
//  SixpackSinday
//
//  Created by Dru Lang on 4/7/14.
//  Copyright (c) 2014 drulang. All rights reserved.
//

#import "NewProfileViewController.h"
#import "DashboardViewController.h"
#import "SixpackSindayAPI.h"
#import "User.h"

@interface NewProfileViewController ()

@property (weak, nonatomic) IBOutlet UITextField *usernameTextField;
@property (weak, nonatomic) IBOutlet UITextField *emailTextField;
@property (weak, nonatomic) IBOutlet UITextField *passwordTextField;
@property (weak, nonatomic) IBOutlet UITextField *confirmPasswordTextField;
@property (weak, nonatomic) IBOutlet UILabel *errorMessageLabel;

@property (strong, nonatomic) User *user;

@end

@implementation NewProfileViewController

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
}



#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([segue.destinationViewController isKindOfClass:[DashboardViewController class]]) {
        DashboardViewController *vc = segue.destinationViewController;
        vc.user = self.user;
    }
}


- (BOOL)shouldPerformSegueWithIdentifier:(NSString *)identifier sender:(id)sender {
    SixpackSindayAPI *api = [[SixpackSindayAPI alloc] init];
    if (self.fieldsValid) {
        self.user = [api createUserWithUserName:self.usernameTextField.text
                                         setEmailTo:self.emailTextField.text
                                      setPasswordTo:self.passwordTextField.text];
        
        
        if (self.user) {
            return YES;
        }
    }
    
    return NO;
}

- (void) setErrorMessage:(NSString *)message {
    self.errorMessageLabel.text = message;
    self.errorMessageLabel.hidden = NO;
}

- (BOOL) fieldsValid {
    
    //Check Username
    if ([self.usernameTextField.text length] == 0 ){
        [self setErrorMessage:@"Username cannot be empty"];
        return NO;
    }
    
    //Check Email
    if ([self.emailTextField.text length] == 0) {
        [self setErrorMessage:@"Email cannot be empty"];
        return NO;
    }
    
    //Check Password
    if (![self.passwordTextField.text isEqualToString:self.confirmPasswordTextField.text]) {
        [self setErrorMessage:@"Passwords do not match"];
        return NO;
    } else if ([self.passwordTextField.text length] == 0) {
        [self setErrorMessage:@"Password cannot be empty"];
        return NO;
    }
    
    self.errorMessageLabel.hidden = YES;
    return YES;

}

@end
